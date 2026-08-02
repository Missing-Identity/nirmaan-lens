from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_id: str
    document_title: str
    page_number: int
    text: str
    parent_id: str
    authority: str
    jurisdictions: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    source_url: str = ""
    source_kind: str = "official"
    printed_page: str | None = None
    effective_from: str | None = None
    effective_to: str | None = None
    token_count: int | None = None
    parser_quality: str = "text"

    @property
    def citation(self) -> str:
        page = self.printed_page or str(self.page_number)
        return f"[{self.source_id} p. {page}]"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Chunk:
        known = cls.__dataclass_fields__.keys()
        return cls(**{key: value[key] for key in known if key in value})


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    rank: int
    score: float
    sparse_score: float
    dense_score: float
    sparse_rank: int | None
    dense_rank: int | None


@dataclass
class QueryResponse:
    question: str
    answer: str
    answer_state: str
    confidence: float
    results: list[SearchResult]
    provider: str
    grounding_valid: bool
    corpus_kind: str
    warnings: list[str] = field(default_factory=list)
