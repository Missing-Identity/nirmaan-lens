from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    data_dir: Path = PROJECT_ROOT / "data"
    raw_dir: Path = PROJECT_ROOT / "data" / "raw"
    processed_dir: Path = PROJECT_ROOT / "data" / "processed"
    chunk_path: Path = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"
    cache_dir: Path = PROJECT_ROOT / ".cache" / "nirmaan_lens"
    artifact_dir: Path = PROJECT_ROOT / "artifacts"
    demo_corpus_path: Path = PROJECT_ROOT / "fixtures" / "demo_corpus.jsonl"
    eval_path: Path = PROJECT_ROOT / "evals" / "silver_v0.1.jsonl"
    manifest_path: Path = PROJECT_ROOT / "sources" / "manifest.json"
    answer_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6-terra")
    embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    offline: bool = os.getenv("NIRMAAN_OFFLINE", "0").lower() in {"1", "true", "yes"}
    chunk_tokens: int = 550
    chunk_overlap: int = 75
    confidence_threshold: float = 0.24

    def ensure_runtime_dirs(self) -> None:
        for path in (
            self.raw_dir,
            self.processed_dir,
            self.cache_dir,
            self.artifact_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
