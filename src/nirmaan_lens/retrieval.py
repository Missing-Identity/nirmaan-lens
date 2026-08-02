from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise
from typing import Protocol

import numpy as np

from nirmaan_lens.config import Settings
from nirmaan_lens.models import Chunk, SearchResult

TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?", re.IGNORECASE)
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "do",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}
EXPANSIONS = {
    "far": ["floor area ratio", "fsi"],
    "fsi": ["floor space index", "far"],
    "oc": ["occupancy certificate"],
    "noc": ["no objection certificate"],
    "setback": ["open space", "building margin"],
    "setbacks": ["open spaces", "building margins"],
    "lake": ["water body", "ftl", "full tank level"],
    "nala": ["storm water drain", "watercourse"],
    "highrise": ["high rise", "building height"],
    "permission": ["building permit", "approval"],
    "tgbpass": ["tsbpass", "building permission self certification"],
    "tsbpass": ["tgbpass", "building permission self certification"],
}


def tokenize(text: str) -> list[str]:
    return [token for token in TOKEN_PATTERN.findall(text.lower()) if token not in STOP_WORDS]


def rewrite_and_expand(query: str) -> str:
    normalized = re.sub(r"\b(tg|ts)[- ]?bpass\b", "tsbpass", query.lower())
    terms = tokenize(normalized)
    additions: list[str] = []
    for term in terms:
        additions.extend(EXPANSIONS.get(term, []))
    return " ".join([normalized, *additions]).strip()


class Embedder(Protocol):
    name: str

    def embed(self, texts: Sequence[str]) -> np.ndarray: ...


class LocalHashEmbedder:
    """Deterministic feature hashing for tests and the zero-cost demo, not a production model."""

    name = "local-hash-384"

    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        matrix = np.zeros((len(texts), self.dimensions), dtype=np.float32)
        for row, text in enumerate(texts):
            tokens = tokenize(rewrite_and_expand(text))
            features = tokens + [f"{a}_{b}" for a, b in pairwise(tokens)]
            for feature in features:
                digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
                value = int.from_bytes(digest, "big")
                index = value % self.dimensions
                sign = 1.0 if value & 1 else -1.0
                matrix[row, index] += sign
            norm = np.linalg.norm(matrix[row])
            if norm:
                matrix[row] /= norm
        return matrix


class CachedOpenAIEmbedder:
    def __init__(self, settings: Settings) -> None:
        from openai import OpenAI

        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        self.model = settings.embedding_model
        self.name = f"openai:{self.model}"
        self.cache_path = settings.cache_dir / f"embeddings-{self.model}.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.client = OpenAI(api_key=settings.openai_api_key)
        self._cache = self._load_cache()

    def _load_cache(self) -> dict[str, list[float]]:
        if not self.cache_path.exists():
            return {}
        try:
            with self.cache_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return {}

    def _key(self, text: str) -> str:
        return hashlib.sha256(f"{self.model}\0{text}".encode()).hexdigest()

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        keys = [self._key(text) for text in texts]
        missing_indexes = [index for index, key in enumerate(keys) if key not in self._cache]
        for batch_start in range(0, len(missing_indexes), 128):
            batch_indexes = missing_indexes[batch_start : batch_start + 128]
            batch_texts = [texts[index] for index in batch_indexes]
            response = self.client.embeddings.create(model=self.model, input=batch_texts)
            for index, item in zip(batch_indexes, response.data, strict=True):
                self._cache[keys[index]] = item.embedding
        if missing_indexes:
            temporary = self.cache_path.with_suffix(".tmp")
            with temporary.open("w", encoding="utf-8") as handle:
                json.dump(self._cache, handle, separators=(",", ":"))
            temporary.replace(self.cache_path)
        return np.asarray([self._cache[key] for key in keys], dtype=np.float32)


def make_embedder(settings: Settings, provider: str = "auto") -> Embedder:
    if provider == "local" or settings.offline:
        return LocalHashEmbedder()
    if provider == "openai":
        return CachedOpenAIEmbedder(settings)
    if provider != "auto":
        raise ValueError(f"unknown embedding provider: {provider}")
    if settings.openai_api_key:
        return CachedOpenAIEmbedder(settings)
    return LocalHashEmbedder()


class BM25:
    def __init__(self, documents: Sequence[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.documents = [tokenize(document) for document in documents]
        self.k1 = k1
        self.b = b
        self.lengths = [len(document) for document in self.documents]
        self.average_length = sum(self.lengths) / max(1, len(self.lengths))
        document_frequency: Counter[str] = Counter()
        for document in self.documents:
            document_frequency.update(set(document))
        count = len(self.documents)
        self.idf = {
            term: math.log(1 + (count - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def scores(self, query: str) -> np.ndarray:
        terms = tokenize(query)
        scores = np.zeros(len(self.documents), dtype=np.float32)
        for index, document in enumerate(self.documents):
            frequencies = Counter(document)
            length_normalizer = self.k1 * (
                1 - self.b + self.b * self.lengths[index] / max(1, self.average_length)
            )
            for term in terms:
                frequency = frequencies.get(term, 0)
                if frequency:
                    scores[index] += self.idf.get(term, 0.0) * (
                        frequency * (self.k1 + 1) / (frequency + length_normalizer)
                    )
        return scores


@dataclass(frozen=True)
class SearchBundle:
    results: list[SearchResult]
    confidence: float
    rewritten_query: str


class HybridRetriever:
    def __init__(self, chunks: Sequence[Chunk], embedder: Embedder) -> None:
        if not chunks:
            raise ValueError("cannot build a retriever with an empty corpus")
        self.chunks = list(chunks)
        self.embedder = embedder
        self.bm25 = BM25([chunk.text for chunk in self.chunks])
        self.embeddings = self.embedder.embed([chunk.text for chunk in self.chunks])
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.embeddings = self.embeddings / np.maximum(norms, 1e-12)

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        authority: str | None = None,
        jurisdiction: str | None = None,
        topic: str | None = None,
        mode: str = "hybrid",
    ) -> SearchBundle:
        rewritten = rewrite_and_expand(query)
        allowed = [
            index
            for index, chunk in enumerate(self.chunks)
            if (not authority or chunk.authority == authority)
            and (not jurisdiction or jurisdiction in chunk.jurisdictions)
            and (not topic or topic in chunk.topics)
        ]
        if not allowed:
            return SearchBundle([], 0.0, rewritten)

        sparse = self.bm25.scores(rewritten)
        query_vector = self.embedder.embed([rewritten])[0]
        query_norm = np.linalg.norm(query_vector)
        if query_norm:
            query_vector = query_vector / query_norm
        dense = self.embeddings @ query_vector

        sparse_order = sorted(allowed, key=lambda index: (-float(sparse[index]), index))
        dense_order = sorted(allowed, key=lambda index: (-float(dense[index]), index))
        sparse_rank = {index: rank for rank, index in enumerate(sparse_order, start=1)}
        dense_rank = {index: rank for rank, index in enumerate(dense_order, start=1)}

        if mode == "dense":
            fused = {index: 1.0 / dense_rank[index] for index in allowed}
        elif mode == "sparse":
            fused = {index: 1.0 / sparse_rank[index] for index in allowed}
        elif mode == "hybrid":
            fused = {
                index: 1 / (60 + sparse_rank[index]) + 1 / (60 + dense_rank[index])
                for index in allowed
            }
        else:
            raise ValueError(f"unknown retrieval mode: {mode}")

        order = sorted(allowed, key=lambda index: (-fused[index], index))[:top_k]
        results = [
            SearchResult(
                chunk=self.chunks[index],
                rank=rank,
                score=float(fused[index]),
                sparse_score=float(sparse[index]),
                dense_score=float(dense[index]),
                sparse_rank=sparse_rank[index],
                dense_rank=dense_rank[index],
            )
            for rank, index in enumerate(order, start=1)
        ]

        query_terms = set(tokenize(rewritten))
        top_terms = set(tokenize(results[0].chunk.text)) if results else set()
        lexical_coverage = len(query_terms & top_terms) / max(1, len(query_terms))
        top_dense = max(0.0, results[0].dense_score) if results else 0.0
        confidence = min(1.0, 0.55 * lexical_coverage + 0.45 * top_dense)
        if results and results[0].sparse_score <= 0 and top_dense < 0.25:
            confidence = 0.0
        return SearchBundle(results, confidence, rewritten)
