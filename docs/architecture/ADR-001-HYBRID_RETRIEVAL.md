# ADR-001: Hybrid Retrieval with Two-Stage Reranking

- **Status:** Proposed
- **Date:** 2026-08-02

## Context

Regulatory queries mix exact lexical identifiers—government-order numbers, rule numbers, table labels, and legal terms—with colloquial paraphrases. Dense-only retrieval can miss identifiers; lexical-only retrieval can miss meaning.

## Decision

Use sparse/BM25 and dense retrieval in parallel, combine results with reciprocal-rank fusion, apply a late-interaction scorer to the fused pool, and use a cross-encoder to select the final top ten child passages. Expand selected children to their parent sections before generation.

## Consequences

- Retrieval quality should improve across both exact and semantic queries.
- Indexing, latency, and operational complexity increase.
- Each stage must be justified by ablation results.
- The system must retain ranks and scores for debugging.
- Rerankers must not bypass authority, jurisdiction, or effective-date filters.

## Rejected alternatives

- Dense-only top-k retrieval: too weak for exact regulatory identifiers.
- BM25-only retrieval: too weak for conversational and multilingual phrasing.
- Cross-encoder over the entire corpus: computationally impractical.
- Generation over isolated chunks: loses exceptions and table context.
