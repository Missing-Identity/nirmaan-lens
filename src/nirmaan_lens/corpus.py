from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path

import requests
import tiktoken
from pypdf import PdfReader

from nirmaan_lens.config import Settings
from nirmaan_lens.io import load_chunks, read_jsonl, write_jsonl
from nirmaan_lens.models import Chunk

ENCODING = tiktoken.get_encoding("o200k_base")


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(
    text: str,
    *,
    chunk_tokens: int = 550,
    overlap_tokens: int = 75,
) -> list[tuple[str, int]]:
    if chunk_tokens < 500:
        raise ValueError("chunk_tokens must be at least 500")
    if overlap_tokens < 50:
        raise ValueError("overlap_tokens must be at least 50")
    if overlap_tokens >= chunk_tokens:
        raise ValueError("overlap_tokens must be smaller than chunk_tokens")

    normalized = normalize_text(text)
    if not normalized:
        return []
    tokens = ENCODING.encode(normalized)
    step = chunk_tokens - overlap_tokens
    chunks: list[tuple[str, int]] = []
    for start in range(0, len(tokens), step):
        window = tokens[start : start + chunk_tokens]
        if not window:
            break
        rendered = normalize_text(ENCODING.decode(window))
        if rendered:
            chunks.append((rendered, len(window)))
        if start + chunk_tokens >= len(tokens):
            break
    return chunks


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fetch_official_sources(settings: Settings, limit: int | None = None) -> list[dict]:
    settings.ensure_runtime_dirs()
    manifest = load_manifest(settings.manifest_path)
    sources = [item for item in manifest["sources"] if item.get("download", True)]
    if limit is not None:
        sources = sources[:limit]

    outcomes: list[dict] = []
    session = requests.Session()
    session.headers["User-Agent"] = "NirmaanLens/0.1 public-interest research"
    for source in sources:
        destination = settings.raw_dir / f"{source['source_id']}.pdf"
        outcome = {"source_id": source["source_id"], "path": str(destination)}
        if destination.exists() and destination.stat().st_size > 1024:
            outcome.update(status="cached", sha256=_sha256(destination))
            outcomes.append(outcome)
            continue
        try:
            response = session.get(source["canonical_url"], timeout=90)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "pdf" not in content_type.lower() and not response.content.startswith(b"%PDF"):
                raise ValueError(f"expected PDF, got {content_type or 'unknown content type'}")
            destination.write_bytes(response.content)
            outcome.update(status="downloaded", sha256=_sha256(destination))
        # One inaccessible source must not prevent the remaining manifest from downloading.
        except Exception as exc:  # noqa: BLE001
            outcome.update(status="failed", error=str(exc))
        outcomes.append(outcome)
    return outcomes


def parse_official_sources(settings: Settings) -> tuple[list[Chunk], list[dict]]:
    settings.ensure_runtime_dirs()
    manifest = load_manifest(settings.manifest_path)
    chunks: list[Chunk] = []
    reports: list[dict] = []

    for source in manifest["sources"]:
        path = settings.raw_dir / f"{source['source_id']}.pdf"
        if not path.exists():
            reports.append({"source_id": source["source_id"], "status": "missing"})
            continue
        try:
            reader = PdfReader(path)
            source_chunks = 0
            low_text_pages = 0
            for page_index, page in enumerate(reader.pages, start=1):
                page_text = normalize_text(page.extract_text() or "")
                if len(page_text) < 80:
                    low_text_pages += 1
                    continue
                for sequence, (text, token_count) in enumerate(
                    chunk_text(
                        page_text,
                        chunk_tokens=settings.chunk_tokens,
                        overlap_tokens=settings.chunk_overlap,
                    ),
                    start=1,
                ):
                    chunks.append(
                        Chunk(
                            chunk_id=f"{source['source_id']}:p{page_index}:c{sequence}",
                            source_id=source["source_id"],
                            document_title=source["title"],
                            page_number=page_index,
                            text=text,
                            parent_id=f"{source['source_id']}:p{page_index}",
                            authority=source["authority"],
                            jurisdictions=source.get("jurisdictions", []),
                            topics=source.get("topics", []),
                            source_url=source["canonical_url"],
                            source_kind="official",
                            effective_from=source.get("effective_from"),
                            token_count=token_count,
                            parser_quality="text",
                        )
                    )
                    source_chunks += 1
            reports.append(
                {
                    "source_id": source["source_id"],
                    "status": "parsed" if source_chunks else "needs_ocr",
                    "pages": len(reader.pages),
                    "chunks": source_chunks,
                    "low_text_pages": low_text_pages,
                    "sha256": _sha256(path),
                }
            )
        # Parser failures are recorded per document so the corpus report remains complete.
        except Exception as exc:  # noqa: BLE001
            reports.append(
                {"source_id": source["source_id"], "status": "failed", "error": str(exc)}
            )

    write_jsonl(settings.chunk_path, (chunk.to_dict() for chunk in chunks))
    write_jsonl(settings.processed_dir / "ingestion_report.jsonl", reports)
    return chunks, reports


def bootstrap_demo(settings: Settings, force: bool = False) -> list[Chunk]:
    settings.ensure_runtime_dirs()
    if settings.chunk_path.exists() and not force:
        existing = load_chunks(settings.chunk_path)
        if existing:
            return existing
    rows = read_jsonl(settings.demo_corpus_path)
    write_jsonl(settings.chunk_path, rows)
    return [Chunk.from_dict(row) for row in rows]


def corpus_summary(chunks: Iterable[Chunk]) -> dict:
    chunks = list(chunks)
    return {
        "chunks": len(chunks),
        "sources": len({chunk.source_id for chunk in chunks}),
        "pages": len({(chunk.source_id, chunk.page_number) for chunk in chunks}),
        "kinds": sorted({chunk.source_kind for chunk in chunks}),
        "generated_at": datetime.now(UTC).isoformat(),
    }
