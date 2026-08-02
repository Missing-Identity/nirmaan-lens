# Dataset Bootstrap Without Architect Contacts

The project can start credibly without an existing network of architects, but it must distinguish regression data from independently reviewed truth.

## Tier 0: synthetic teaching fixtures

`fixtures/demo_corpus.jsonl` contains 16 authored chunks across five synthetic source families. They exercise page citations, abbreviations, missing facts, jurisdiction, water bodies, fire NOC, permission workflow, zoning, and safety boundaries.

They are deliberately labeled `source_kind=synthetic` in every record and in the UI. They must never be used as legal or architectural authority.

`evals/silver_v0.1.jsonl` contains 60 cases:

- 50 answerable retrieval cases;
- 10 unanswerable, false-premise, out-of-domain, or prompt-injection cases;
- boundary, ambiguity, query-expansion, conflict, and scope slices.

This tier lets contributors build the harness, catch regressions, test abstention, and compare pipelines immediately.

## Tier 1: official-document silver set

The next dataset uses the tracked source manifest and is still possible without professional contacts:

1. Download and hash official PDFs.
2. Record source title, issuing authority, publication date, URL, and PDF page count.
3. Select clauses, definitions, tables, exceptions, and amendment statements that are explicit in the text.
4. Write questions whose expected evidence can be verified directly on an exact PDF page.
5. Add threshold pairs such as just below, exactly at, and just above a stated boundary.
6. Add “should return nothing” questions for nonexistent GOs, false clauses, unrelated domains, and missing evidence.
7. Mark every label `silver-unreviewed` and keep the reviewer field empty.

Good silver cases test retrieval of explicit text. They should not assert that a real plot is compliant when jurisdiction, current applicability, professional interpretation, or external evidence remains unresolved.

## Tier 2: independently reviewed gold set

A case becomes gold only when a second person independently verifies:

- the exact official document and immutable version;
- the PDF and printed page mapping;
- the controlling clause or table;
- temporal and jurisdiction applicability;
- expected answer state and required clarifications;
- any relevant amendment or conflict.

The first reviewers do not have to be personal contacts. Possible routes include a paid one-hour review from a licensed architect or town planner, a university planning faculty collaboration, an open-source contributor with disclosed credentials, or a structured outreach request to small practices. Reviewer identity and role are stored; disagreements are adjudicated rather than averaged.

## Testing we can own now

- Parser tests: page count, empty-page rate, OCR flags, repeated headers, tables, and text corruption.
- Chunk tests: maximum tokens, minimum overlap, page identity, and parent identity.
- Retrieval tests: Hit Rate, MRR, NDCG, evidence-set recall, and filter correctness.
- Grounding tests: valid citations, fabricated page rejection, uncited-answer rejection, and prompt injection in retrieved text.
- Abstention tests: unrelated questions, nonexistent sources, false premises, and missing decision-critical facts.
- Cache tests: cold/warm embedding calls, hit rate, latency, and invalidation after model or content changes.
- Product tests: source-kind warning visibility, evidence inspection, and no-approval-guarantee language.

## Promotion rule

Never rename a synthetic or single-review silver set “golden” to satisfy a project bullet point. Report its actual status, build the 50+ case machinery now, and promote cases individually when independent review evidence exists.

