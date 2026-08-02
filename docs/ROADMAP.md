# Roadmap and Initial Work Breakdown

## Delivery strategy

Build depth before breadth. The first public demonstration should answer a narrow set of Hyderabad building-rule questions extremely well, show why each retrieval stage helps, and refuse unsupported conclusions.

## Milestone 0 — Validate the problem and freeze scope

**Goal:** Confirm the recurring user workflow and choose the exact MVP jurisdiction/document chain.

Deliverables:

- Interview guide and consent-safe notes template
- 10–15 interviews across architects, engineers, consultants, small builders, and homeowners
- At least 100 de-identified real questions
- Ranked user jobs and failure costs
- MVP jurisdiction decision
- Initial authoritative source manifest

Exit criteria:

- At least five domain professionals agree to test the prototype.
- Source access is lawful and technically feasible without bypassing controls.
- The MVP has explicit document and topic boundaries.

## Milestone 1 — Build the corpus foundation

**Goal:** Create a reproducible, page-aware, versioned corpus.

Deliverables:

- Source-registry schema
- Acquisition manifest and checksum workflow
- Native PDF and OCR parser comparison
- Page, heading, table, footnote, and bounding-box extraction
- Parent/child chunker at 550–700 tokens with at least 75 overlap
- Temporal and amendment graph
- Corpus QA report for the first 30–50 documents

Exit criteria:

- Every searchable chunk resolves to an immutable file and exact page.
- Table and OCR failure rates are measured.
- No unresolved-source document is promoted silently.

## Milestone 2 — Establish naive RAG and golden-set v0.1

**Goal:** Create a credible baseline before optimisation.

Deliverables:

- Dense top-5 baseline
- First 30 development cases and 10 negative cases
- Retrieval metric computation
- Query/evidence inspection interface
- Baseline latency and failure report

Exit criteria:

- Baseline run is reproducible from pinned corpus and configuration.
- Retrieval failures are categorised rather than manually hidden.

## Milestone 3 — Advanced retrieval

**Goal:** Implement and justify the full retrieval pipeline.

Deliverables:

- BM25/sparse index and rank fusion
- Query normalisation, rewriting, and expansion
- Temporal, authority, jurisdiction, and topic filtering
- Late-interaction scoring
- Cross-encoder reranking to top ten
- Parent-section expansion
- B0–B6 ablation report

Exit criteria:

- Hit Rate@10, MRR@10, and NDCG@10 targets are met or gaps are documented.
- Each retained stage shows measurable value on at least one important slice.

## Milestone 4 — Proposal checks and grounding

**Goal:** Produce safe, reproducible preliminary answers.

Deliverables:

- Structured query and proposal-fact contract
- Initial reviewed deterministic rules
- Claim-to-evidence response format
- Citation verifier
- Confidence policy and answer-state router
- Clarification and abstention behavior
- Official-domain fallback

Exit criteria:

- Encoded calculations pass all boundary tests.
- Citation precision and abstention targets are met on the development set.
- No critical unsupported claim passes the verifier in the reviewed demo suite.

## Milestone 5 — Evaluation dashboard and public benchmark

**Goal:** Make retrieval quality inspectable.

Deliverables:

- Golden set v1 with at least 60 reviewed cases
- Private holdout methodology
- Baseline/ablation comparison dashboard
- Slice metrics, latency waterfall, caching, and failure explorer
- Reproducible benchmark report

Exit criteria:

- Full run can be reproduced from versioned inputs.
- Improvement claims link to measured results and configurations.

## Milestone 6 — Interview-ready public demo

**Goal:** Deliver a polished project that demonstrates product and engineering judgment.

Deliverables:

- Ask-a-rule interface
- Proposal-check interface
- Before/after amendment comparison
- Evidence drawer with page preview
- Three signature demo scenarios
- Architecture walkthrough and recorded demonstration
- Deployment, security, and contribution documentation

Exit criteria:

- A new evaluator can reproduce the demo and benchmark.
- Domain testers review the product's limitations and evidence UX.

## Suggested eight-week sequence

| Week | Focus |
|---|---|
| 1 | Interviews, source access, jurisdiction decision |
| 2 | Registry, ingestion pilot, parser benchmark |
| 3 | Chunking, corpus QA, naive baseline |
| 4 | Hybrid retrieval, filters, query rewriting |
| 5 | Late interaction, reranking, parent retrieval |
| 6 | Rule engine, grounding, confidence, fallback |
| 7 | 60-case evaluation, adversarial suite, dashboard |
| 8 | Product UX, benchmark narrative, deployment and demo |

## Issue-ready initial backlog

| Priority | Issue title | Milestone | Suggested labels |
|---:|---|---|---|
| P0 | Conduct 10–15 Hyderabad building-permission workflow interviews | M0 | research, product |
| P0 | Freeze the MVP jurisdiction and regulatory topics | M0 | decision, scope |
| P0 | Create the authoritative source manifest | M0 | corpus, provenance |
| P0 | Define the source registry and temporal amendment schema | M1 | architecture, data |
| P0 | Benchmark PDF/OCR parsers on ten representative documents | M1 | ingestion, experiment |
| P0 | Implement and evaluate page-aware hierarchical chunking | M1 | retrieval, ingestion |
| P1 | Build corpus QA checks for pages, tables, OCR, and checksums | M1 | quality, ingestion |
| P0 | Assemble golden-set v0.1 with 40 reviewed cases | M2 | evaluation |
| P0 | Establish the dense top-5 naive RAG baseline | M2 | retrieval, baseline |
| P1 | Add query-level evidence inspection | M2 | evaluation, tooling |
| P0 | Add BM25 and reciprocal-rank fusion | M3 | retrieval |
| P0 | Add temporal and jurisdiction filtering | M3 | retrieval, temporal |
| P1 | Evaluate query rewriting versus expansion | M3 | retrieval, experiment |
| P1 | Evaluate late interaction and cross-encoder reranking | M3 | retrieval, experiment |
| P1 | Add parent-section expansion | M3 | retrieval |
| P0 | Define structured proposal facts and required-field validation | M4 | product, rule-engine |
| P0 | Implement the first reviewed deterministic rule set | M4 | rule-engine, safety |
| P0 | Add claim-level citation verification and answer states | M4 | grounding, safety |
| P1 | Implement official-domain web fallback | M4 | fallback, provenance |
| P0 | Expand the golden set to 60+ cases and freeze v1 | M5 | evaluation |
| P1 | Build the retrieval-quality dashboard | M5 | dashboard, evaluation |
| P0 | Publish the naive-versus-advanced benchmark report | M5 | benchmark, docs |

## Project risks to track

- Dynamic or restricted government portals may limit reproducible acquisition.
- Printed and PDF page numbers may differ.
- Scanned tables and amendments may require manual review.
- Jurisdiction changes can make locality mapping temporally complex.
- Domain experts are needed to validate controlling sources and negative cases.
- Late interaction may not justify its operating cost on a small corpus.
- A broad geospatial promise could overwhelm the text-RAG MVP.
