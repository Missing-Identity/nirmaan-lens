# Implementation Status

## Shipped in v0.1

| Requirement | Status | Current implementation |
|---|---|---|
| Windows-first local development | Shipped | `nirmaan.cmd` + PowerShell command runner, Windows venv paths, Windows CI release gate |
| Page-number citations | Shipped | Page-first parsing, citation keys, evidence display, allow-list validation |
| Hybrid dense + sparse retrieval | Shipped | BM25 + OpenAI embeddings/local test vectors + reciprocal-rank fusion |
| Chunking >=500/50 | Shipped | 550-token children with 75-token overlap and enforced minimums |
| Query expansion | Shipped, rules-first | Domain aliases for OC, NOC, FTL, FAR/FSI, setbacks, high-rise, TS-bPASS |
| Metadata filtering | Shipped | Authority, jurisdiction, and topic filters in the retriever; authority/topic in UI |
| Citation grounding | Shipped | Evidence-only prompt, exact citation allow-list, fallback on invalid citations |
| 50+ evaluation cases | Shipped as silver | 60 synthetic unreviewed cases; gold promotion requires independent review |
| Hit Rate, MRR, NDCG | Shipped | CLI artifact and Streamlit dashboard |
| Query rewriting | Partial | Alias normalization and expansion; LLM ambiguity classification is planned |
| Parent retrieval | Shipped at page level | Sibling chunks from top parent pages; section hierarchy is planned |
| Embedding cache | Shipped | Model + content SHA-256 cache; 80% latency goal not yet benchmarked on official corpus |
| Dashboard | Shipped | Ask, evidence ranks, scores, sources, benchmark comparison |
| Adversarial nothing cases | Shipped | 10 false-premise, injection, and out-of-domain cases plus unit tests |
| Chunking documentation | Shipped | `docs/CHUNKING_STRATEGY.md` |
| Naive RAG comparison | Shipped on synthetic suite | Dense top-5 versus hybrid top-10; official benchmark is next |

## Planned and not claimed as complete

| Requirement | Target stage | Acceptance evidence |
|---|---|---|
| Cross-encoder reranking | v0.2 | Top-10 reranker ablation improves official MRR/NDCG after latency measurement |
| ColBERT / late interaction | v0.3 | Beats or complements cross-encoder on tables, long clauses, and multilingual queries |
| Official web-search fallback | v0.3 | Approved-domain-only search, provenance admission, confidence policy, audit log |
| Full ambiguous-query rewriting | v0.2 | Clarification accuracy on missing authority/date/road-width/height cases |
| Section-level parent documents | v0.2 | Page-traceable hierarchy and evidence-set recall improvement |
| OCR and layout/table extraction | v0.2 | Parser benchmark and OCR/table evaluation slice |
| Temporal amendment graph | v0.3 | As-of-date applicability tests across base rules and amendments |
| Independently reviewed gold set | continuous | At least 50 cases with reviewer role, source version, exact pages, adjudication |
| >=80% warm embedding-stage reduction | v0.2 benchmark | Defined cold/warm workload with cache hits, p50/p95, and invalidation tests |

The project treats every advanced retrieval component as an ablation candidate. A technique is promoted to the default pipeline only when it improves the frozen benchmark enough to justify its cost and latency.
