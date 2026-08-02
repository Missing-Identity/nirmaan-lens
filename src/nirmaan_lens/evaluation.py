from __future__ import annotations

import math
import time
from collections.abc import Sequence

from nirmaan_lens.config import Settings
from nirmaan_lens.io import read_jsonl, write_json
from nirmaan_lens.models import Chunk, SearchResult
from nirmaan_lens.retrieval import HybridRetriever, make_embedder


def _is_relevant(result: SearchResult, case: dict) -> bool:
    expected_chunks = set(case.get("expected_chunk_ids", []))
    expected_sources = set(case.get("expected_source_ids", []))
    return result.chunk.chunk_id in expected_chunks or (
        not expected_chunks and result.chunk.source_id in expected_sources
    )


def _query_metrics(
    results: Sequence[SearchResult], case: dict, k: int
) -> tuple[float, float, float]:
    relevance = [1.0 if _is_relevant(result, case) else 0.0 for result in results[:k]]
    hit = float(any(relevance))
    reciprocal_rank = next((1.0 / rank for rank, rel in enumerate(relevance, start=1) if rel), 0.0)
    dcg = sum(rel / math.log2(rank + 1) for rank, rel in enumerate(relevance, start=1))
    relevant_count = max(
        1, len(case.get("expected_chunk_ids") or case.get("expected_source_ids", []))
    )
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(k, relevant_count) + 1))
    ndcg = dcg / ideal if ideal else 0.0
    return hit, reciprocal_rank, ndcg


def evaluate_retriever(
    retriever: HybridRetriever,
    cases: Sequence[dict],
    *,
    mode: str,
    top_k: int,
    confidence_threshold: float,
) -> dict:
    answerable_rows: list[tuple[float, float, float]] = []
    no_answer_true_positive = 0
    no_answer_false_positive = 0
    no_answer_false_negative = 0
    query_rows: list[dict] = []
    started = time.perf_counter()

    for case in cases:
        bundle = retriever.search(case["question"], top_k=top_k, mode=mode)
        predicted_unanswerable = not bundle.results or bundle.confidence < confidence_threshold
        expected_unanswerable = case["expected_answer_state"] == "not_found"
        if expected_unanswerable:
            if predicted_unanswerable:
                no_answer_true_positive += 1
            else:
                no_answer_false_negative += 1
            metrics = (0.0, 0.0, 0.0)
        else:
            if predicted_unanswerable:
                no_answer_false_positive += 1
            metrics = _query_metrics(bundle.results, case, top_k)
            answerable_rows.append(metrics)
        query_rows.append(
            {
                "case_id": case["case_id"],
                "slice": case["slice"],
                "question": case["question"],
                "expected_answer_state": case["expected_answer_state"],
                "predicted_unanswerable": predicted_unanswerable,
                "confidence": round(bundle.confidence, 4),
                "hit": metrics[0],
                "first_result": bundle.results[0].chunk.chunk_id if bundle.results else None,
            }
        )

    elapsed = time.perf_counter() - started
    denominator = max(1, len(answerable_rows))
    precision_denominator = no_answer_true_positive + no_answer_false_positive
    recall_denominator = no_answer_true_positive + no_answer_false_negative
    precision = no_answer_true_positive / precision_denominator if precision_denominator else 0.0
    recall = no_answer_true_positive / recall_denominator if recall_denominator else 0.0
    abstention_f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "mode": mode,
        "top_k": top_k,
        "case_count": len(cases),
        "answerable_count": len(answerable_rows),
        "hit_rate": sum(row[0] for row in answerable_rows) / denominator,
        "mrr": sum(row[1] for row in answerable_rows) / denominator,
        "ndcg": sum(row[2] for row in answerable_rows) / denominator,
        "abstention_precision": precision,
        "abstention_recall": recall,
        "abstention_f1": abstention_f1,
        "elapsed_seconds": elapsed,
        "milliseconds_per_query": elapsed * 1000 / max(1, len(cases)),
        "queries": query_rows,
    }


def run_benchmark(chunks: Sequence[Chunk], settings: Settings, provider: str = "local") -> dict:
    cases = read_jsonl(settings.eval_path)
    embedder = make_embedder(settings, provider)
    retriever = HybridRetriever(chunks, embedder)
    baseline = evaluate_retriever(
        retriever,
        cases,
        mode="dense",
        top_k=5,
        confidence_threshold=settings.confidence_threshold,
    )
    hybrid = evaluate_retriever(
        retriever,
        cases,
        mode="hybrid",
        top_k=10,
        confidence_threshold=settings.confidence_threshold,
    )
    result = {
        "dataset": settings.eval_path.name,
        "dataset_status": "silver-synthetic-unreviewed",
        "embedding_provider": embedder.name,
        "baseline": baseline,
        "hybrid": hybrid,
        "improvement": {
            metric: hybrid[metric] - baseline[metric] for metric in ("hit_rate", "mrr", "ndcg")
        },
    }
    write_json(settings.artifact_dir / "eval-latest.json", result)
    return result
