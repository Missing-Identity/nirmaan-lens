from __future__ import annotations

import argparse
import json
import platform
import sys

from nirmaan_lens.config import Settings
from nirmaan_lens.corpus import (
    bootstrap_demo,
    corpus_summary,
    fetch_official_sources,
    parse_official_sources,
)
from nirmaan_lens.evaluation import run_benchmark
from nirmaan_lens.io import load_chunks
from nirmaan_lens.service import NirmaanLensService


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nirmaan-lens")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("bootstrap-demo", help="install the bundled synthetic demo corpus")
    demo.add_argument("--force", action="store_true", help="replace the current processed corpus")

    fetch = subparsers.add_parser("fetch-official", help="download official PDFs from the manifest")
    fetch.add_argument("--limit", type=int)

    subparsers.add_parser("ingest-official", help="parse downloaded PDFs into page-aware chunks")

    evaluation = subparsers.add_parser("eval", help="run the retrieval benchmark")
    evaluation.add_argument("--provider", choices=["local", "openai"], default="local")

    ask = subparsers.add_parser("ask", help="ask one question from the terminal")
    ask.add_argument("question")
    ask.add_argument("--provider", choices=["auto", "local", "openai"], default="auto")
    ask.add_argument("--no-generation", action="store_true")

    subparsers.add_parser("doctor", help="check the local environment and corpus")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = Settings()
    settings.ensure_runtime_dirs()

    if args.command == "bootstrap-demo":
        chunks = bootstrap_demo(settings, force=args.force)
        _print({"status": "ready", **corpus_summary(chunks), "path": settings.chunk_path})
        return
    if args.command == "fetch-official":
        _print(fetch_official_sources(settings, limit=args.limit))
        return
    if args.command == "ingest-official":
        chunks, report = parse_official_sources(settings)
        _print({"corpus": corpus_summary(chunks), "report": report})
        return
    if args.command == "eval":
        chunks = load_chunks(settings.chunk_path) or bootstrap_demo(settings)
        _print(run_benchmark(chunks, settings, provider=args.provider))
        return
    if args.command == "ask":
        chunks = load_chunks(settings.chunk_path) or bootstrap_demo(settings)
        service = NirmaanLensService(
            chunks,
            settings,
            embedding_provider=args.provider,
            use_generation=not args.no_generation,
        )
        response = service.answer(args.question)
        _print(
            {
                "answer_state": response.answer_state,
                "confidence": response.confidence,
                "answer": response.answer,
                "warnings": response.warnings,
                "results": [
                    {
                        "rank": result.rank,
                        "citation": result.chunk.citation,
                        "chunk_id": result.chunk.chunk_id,
                        "score": result.score,
                    }
                    for result in response.results
                ],
            }
        )
        return
    if args.command == "doctor":
        chunks = load_chunks(settings.chunk_path)
        _print(
            {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "openai_key_configured": bool(settings.openai_api_key),
                "answer_model": settings.answer_model,
                "embedding_model": settings.embedding_model,
                "offline": settings.offline,
                "corpus": corpus_summary(chunks) if chunks else None,
                "next_step": "nirmaan-lens bootstrap-demo"
                if not chunks
                else "streamlit run app.py",
            }
        )


if __name__ == "__main__":
    main()
