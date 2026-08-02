# Core Data Contracts

This document defines implementation-neutral logical fields. Concrete database and API schemas will be derived after the source pilot.

## Source record

| Field | Meaning |
|---|---|
| `source_id` | Stable internal identifier |
| `authority_name` | Issuing body |
| `authority_tier` | Source-policy authority tier |
| `canonical_url` | Verified official location |
| `retrieved_at` | Acquisition timestamp |
| `content_hash` | Identity of acquired bytes |
| `rights_class` | Retention/redistribution classification |
| `admission_state` | Quarantined, reviewed, admitted, or withdrawn |

## Document version

| Field | Meaning |
|---|---|
| `document_id` | Stable document family identifier |
| `version_id` | Immutable acquired version |
| `title` | Official title |
| `document_number` | GO, Act, memo, rule, order, or notification number |
| `document_type` | Controlled type |
| `published_on` | Publication date if known |
| `effective_from` | First applicable date if established |
| `effective_to` | Last applicable date if established |
| `jurisdictions` | Applicable authorities/areas |
| `topics` | Controlled regulatory topics |
| `language` | Source language |
| `page_count` | Stored PDF page count |
| `parser_version` | Reproducibility field |
| `review_state` | Metadata review status |

## Document relationship

| Field | Meaning |
|---|---|
| `from_version_id` | Later or referring source |
| `relationship` | Amends, clarifies, supersedes, cites, or implements |
| `to_version_id` | Earlier or referenced source |
| `scope` | Whole document or clause/table-level scope |
| `evidence_page` | Page establishing the relationship |
| `review_state` | Inferred, reviewed, or disputed |

## Page and chunk

Every searchable chunk retains:

- source/document/version identity;
- PDF page index and printed page number;
- bounding boxes or text offsets;
- parent section and hierarchy path;
- child sequence and overlap region;
- table/footnote flags;
- OCR and parser quality;
- temporal, authority, jurisdiction, and topic metadata;
- representation model versions.

## Structured proposal facts

| Field | Required when relevant |
|---|---|
| `locality` | Always captured, even if authority is supplied |
| `authority` | Required for unconditional jurisdiction-specific output |
| `as_of_date` | Required for temporal answer; defaults must be visible |
| `plot_area` and unit | Proposal checks |
| `plot_dimensions` and unit | Envelope calculations |
| `road_width` and unit | Height/setback/pathway questions where controlling |
| `proposed_use` | Proposal checks |
| `proposed_height` and unit | Height/high-rise/NOC questions |
| `proposed_floors` | User comprehension and cross-checking |
| `corner_plot` | When road-side rules may apply to multiple edges |
| `user_documents` | Optional private evidence references |

Fields retain both the original user value and normalized value.

## Answer contract

| Field | Meaning |
|---|---|
| `answer_state` | Supported, conditional, clarification, conflict, not-found, or professional-review |
| `as_of_date` | Date used for applicability |
| `authority_assumption` | Resolved authority and confidence |
| `direct_answer` | Concise user-facing result |
| `claims` | Material claims and evidence links |
| `calculations` | Deterministic traces and input provenance |
| `conditions` | Facts that may change the result |
| `missing_fields` | Targeted clarification list |
| `conflicts` | Source/version conflicts |
| `confidence_factors` | Explainable support and limitation factors |
| `corpus_version` | Reproducibility field |
| `pipeline_version` | Reproducibility field |

## Claim contract

Each material claim contains:

- claim text and type;
- evidence passage IDs;
- cited source/pages;
- applicable date and jurisdiction check;
- deterministic trace IDs where relevant;
- support-verification result;
- contradiction/conflict state;
- rendering decision: include, qualify, or suppress.
