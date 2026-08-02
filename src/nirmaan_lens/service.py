from __future__ import annotations

from collections.abc import Sequence

from nirmaan_lens.config import Settings
from nirmaan_lens.generation import (
    ABSTENTION,
    GroundedGenerator,
    extractive_answer,
    validate_citations,
)
from nirmaan_lens.models import Chunk, QueryResponse, SearchResult
from nirmaan_lens.retrieval import HybridRetriever, make_embedder


class NirmaanLensService:
    def __init__(
        self,
        chunks: Sequence[Chunk],
        settings: Settings,
        *,
        embedding_provider: str = "auto",
        use_generation: bool = True,
    ) -> None:
        self.chunks = list(chunks)
        self.settings = settings
        self.embedder = make_embedder(settings, embedding_provider)
        self.retriever = HybridRetriever(self.chunks, self.embedder)
        self.generator = None
        if use_generation and settings.openai_api_key and not settings.offline:
            self.generator = GroundedGenerator(settings)

    def _parent_evidence(self, results: Sequence[SearchResult], max_chunks: int = 8) -> list[Chunk]:
        selected: list[Chunk] = []
        seen: set[str] = set()
        top_parents = {result.chunk.parent_id for result in results[:5]}
        for result in results[:5]:
            if result.chunk.chunk_id not in seen:
                selected.append(result.chunk)
                seen.add(result.chunk.chunk_id)
        for chunk in self.chunks:
            if chunk.parent_id in top_parents and chunk.chunk_id not in seen:
                selected.append(chunk)
                seen.add(chunk.chunk_id)
            if len(selected) >= max_chunks:
                break
        return selected[:max_chunks]

    def answer(
        self,
        question: str,
        *,
        authority: str | None = None,
        jurisdiction: str | None = None,
        topic: str | None = None,
    ) -> QueryResponse:
        bundle = self.retriever.search(
            question,
            top_k=10,
            authority=authority,
            jurisdiction=jurisdiction,
            topic=topic,
        )
        corpus_kind = (
            "synthetic"
            if bundle.results and all(r.chunk.source_kind == "synthetic" for r in bundle.results)
            else "official"
        )
        if not bundle.results or bundle.confidence < self.settings.confidence_threshold:
            return QueryResponse(
                question=question,
                answer=ABSTENTION,
                answer_state="not_found",
                confidence=bundle.confidence,
                results=bundle.results,
                provider=self.embedder.name,
                grounding_valid=True,
                corpus_kind=corpus_kind,
            )

        evidence = self._parent_evidence(bundle.results)
        warnings: list[str] = []
        if corpus_kind == "synthetic":
            warnings.append("This answer uses synthetic demo fixtures, not controlling law.")
        if self.generator is None:
            answer = extractive_answer(bundle.results, "generation disabled")
            return QueryResponse(
                question=question,
                answer=answer,
                answer_state="evidence_only",
                confidence=bundle.confidence,
                results=bundle.results,
                provider=self.embedder.name,
                grounding_valid=True,
                corpus_kind=corpus_kind,
                warnings=warnings,
            )

        try:
            answer = self.generator.generate(question, evidence)
            grounding_valid, errors = validate_citations(answer, evidence)
            if not grounding_valid:
                warnings.extend(errors)
                answer = extractive_answer(bundle.results, "generated citations failed validation")
                state = "grounding_failed"
            else:
                state = "supported"
        # Model/network failures deliberately degrade to retrieved evidence instead of a 500.
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Answer generation failed: {type(exc).__name__}")
            answer = extractive_answer(bundle.results, "answer generation failed")
            grounding_valid = True
            state = "evidence_only"

        return QueryResponse(
            question=question,
            answer=answer,
            answer_state=state,
            confidence=bundle.confidence,
            results=bundle.results,
            provider=self.embedder.name,
            grounding_valid=grounding_valid,
            corpus_kind=corpus_kind,
            warnings=warnings,
        )
