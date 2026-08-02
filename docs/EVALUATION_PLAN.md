# Evaluation and Benchmark Plan

## Objective

Demonstrate that the advanced retrieval and grounding pipeline improves evidence retrieval and answer safety over a naive RAG baseline.

The evaluation is retrieval-first. An eloquent answer cannot compensate for missing controlling evidence.

## Golden-set composition

The initial reviewed set contains at least 60 cases.

| Slice | Count | What it tests |
|---|---:|---|
| Exact rule/table lookup | 10 | GO numbers, clause identifiers, tables, defined terms |
| Amendment and temporal reasoning | 10 | Base rule plus one or more amendments, as-of dates |
| Proposal scenarios | 10 | Structured inputs, units, thresholds, deterministic traces |
| Ambiguity and language variation | 10 | Missing facts, colloquial English, Hinglish/Telugu terminology variants |
| OCR and table retrieval | 10 | Scans, page-spanning tables, footnotes, extraction quality |
| Unanswerable and adversarial | 10 | False premises, nonexistent sources, prompt injection, out-of-scope requests |

The set may grow, but slice membership and version history are immutable for a published benchmark release.

## Case contract

Each case stores:

- stable case ID and dataset version;
- question and optional conversation context;
- structured proposal facts and as-of date;
- expected answer state;
- relevant source IDs and page ranges;
- graded relevance per evidence item;
- expected factual propositions;
- forbidden or unsupported propositions;
- required clarification fields;
- deterministic expected result and trace, where applicable;
- difficulty, language, topic, jurisdiction, and document-quality tags;
- reviewer identity/role and adjudication state.

## Ground-truth creation

1. Collect real questions from domain interviews.
2. A project contributor maps candidate official sources.
3. A domain reviewer validates applicability, pages, and expected answer state.
4. Disagreement is recorded and adjudicated; it is not averaged away.
5. Cases with unresolved controlling-source conflicts remain a dedicated conflict slice, not ordinary answerable cases.

## Retrieval metrics

### Hit Rate@k

Fraction of answerable queries with at least one relevant evidence item in the top `k`.

### MRR@10

Mean reciprocal rank of the first relevant evidence item, capped at ten.

### NDCG@10

Measures ranking quality when multiple passages have different relevance grades.

### Evidence-set recall

Fraction of required evidence groups retrieved. This catches multi-document questions where retrieving only the base rule is insufficient.

Metrics are reported overall and by evaluation slice, source family, language, OCR quality, and query type.

## Answer and safety metrics

- **Citation precision:** supported material citations divided by all material citations.
- **Citation coverage:** material claims with adequate citations divided by all material claims.
- **Grounded-claim rate:** verified material claims divided by generated material claims.
- **Factual completeness:** expected propositions present without contradiction.
- **Abstention precision/recall/F1:** correct handling of unanswerable or unsafe cases.
- **Clarification accuracy:** correct identification of missing decision-critical fields.
- **Temporal applicability accuracy:** correct source version for the requested date.
- **Calculation accuracy:** exact match on deterministic results and trace conditions.

## Latency and cost metrics

Record p50 and p95 for:

- query understanding;
- sparse retrieval;
- dense retrieval;
- late interaction;
- cross-encoder reranking;
- parent expansion;
- deterministic evaluation;
- answer generation;
- grounding verification;
- complete request.

Also record embedding cache hit rate, query-result cache hit rate, model-token usage, index size, and cost per evaluated query.

The 80% caching objective applies to repeated embedding-stage latency under a defined warm-cache workload. It is not presented as an achieved end-to-end reduction unless measured.

## Baseline and ablation ladder

| ID | Pipeline |
|---|---|
| B0 | 550-token chunks, dense retrieval, top five, direct generation |
| B1 | B0 plus BM25 and reciprocal-rank fusion |
| B2 | B1 plus temporal/jurisdiction metadata filters |
| B3 | B2 plus query rewriting and expansion |
| B4 | B3 plus late-interaction scoring |
| B5 | B4 plus cross-encoder reranking |
| B6 | B5 plus parent-section expansion |
| B7 | B6 plus deterministic rules, grounding, confidence, and abstention |

Every benchmark run freezes:

- corpus version;
- golden-set version;
- model names and revisions;
- parser/chunker configuration;
- retrieval weights and candidate sizes;
- hardware and concurrency;
- cache state;
- prompts and generation parameters.

## Initial release targets

| Metric | Target |
|---|---:|
| Hit Rate@10 | >= 0.90 |
| MRR@10 | >= 0.75 |
| NDCG@10 | >= 0.80 |
| Citation precision | >= 0.95 |
| Abstention F1 | >= 0.85 |
| Temporal applicability accuracy | >= 0.90 |
| Deterministic calculation accuracy | 1.00 on encoded MVP rules |
| Warm-cache embedding-stage reduction | >= 80% |

Targets may be revised after the pilot only with a documented reason. Results must never be backfilled into targets.

## Adversarial suite

Include cases that:

- name a nonexistent GO or fabricate a clause;
- demand an answer without citations;
- tell the model to ignore safety or source policy;
- embed instructions inside a retrieved/uploaded document;
- ask for a definitive answer with missing road width or authority;
- cite an outdated rule as current;
- conflate printed page numbers and PDF indices;
- exploit unit boundaries or just-below/just-above thresholds;
- ask an unrelated legal, medical, or political question;
- request an approval guarantee.

## Dashboard

The retrieval-quality dashboard will show:

- baseline versus current metrics;
- slice-level heatmap;
- metric history by corpus and pipeline version;
- most common failure categories;
- query-level rank/evidence inspection;
- citation failures and source conflicts;
- latency waterfall and cache outcomes;
- official-web fallback and abstention rates;
- OCR quality versus retrieval performance.

## Leakage controls

- Keep a private holdout set not used during prompt or weight tuning.
- Do not include answer keys in indexed retrieval content.
- Separate domain-interview questions from benchmark labels.
- Publish the development set and methodology before publishing final holdout results.
- Report repeated tuning against the same set as development performance, not independent validation.
