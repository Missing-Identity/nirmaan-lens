# Source and Provenance Policy

## Purpose

NirmaanLens can be trusted only if users can distinguish authoritative evidence, current applicability, user-supplied facts, and unverified fallback material. This policy governs acquisition, ranking, citation, freshness, and redistribution.

## Authority tiers

### Tier 1 — controlling official material

- Acts, rules, gazettes, government orders, notifications, and official amendments
- Official master plans, zoning regulations, lake notifications, and authority-issued maps
- Official departmental procedures and NOC requirements
- Official regulatory orders and judgments

Tier 1 material may support a material regulatory claim when its applicability is established.

### Tier 2 — official explanatory material

- Government FAQs
- Citizen guidance, checklists, and timelines
- Official portal help text
- Department presentations or explanatory circulars that do not themselves create a rule

Tier 2 may explain procedure but must not silently override Tier 1.

### Tier 3 — professional or secondary reference

- Practitioner articles
- Calculators and commercial compliance tools
- Academic commentary
- Reputable news reports

Tier 3 is useful for terminology discovery, test-question collection, and identifying likely amendments. It does not control a proposal answer and is not used by the production answer path unless clearly labelled as non-authoritative commentary.

### Tier 4 — user-supplied material

- Plans, letters, approvals, notices, and project documents uploaded by a user

Tier 4 supports statements about that user's document. It is never promoted to the shared public corpus and cannot establish a general rule.

## Initial official source families

| Source family | Initial purpose | Expected authority |
|---|---|---|
| Telangana BuildNow GO/Act repository | Base rules, Acts, amendments, jurisdiction changes | Tier 1 |
| TG-bPASS | Permission routes, official guidance, checklists, timelines | Tier 1–2 |
| HMDA | Master plans, zoning, notifications, planning Acts | Tier 1 |
| HMDA Lakes | Lake and buffer-zone notifications and mapped records | Tier 1 |
| Telangana Fire and Emergency Services | Fire Act, NOC procedures, circulars | Tier 1–2 |
| Telangana RERA | Rules, orders, judgments, notices, public project material | Tier 1–2 |

The corpus manifest will list exact documents. A domain homepage is not sufficient provenance.

## Source admission checklist

Before a document becomes searchable:

- The publisher and official domain are verified.
- The canonical URL and retrieval timestamp are recorded.
- File type, checksum, and byte length are recorded.
- Title, document number, publication date, and effective date are extracted or marked unknown.
- Jurisdiction and subject scope are assigned with review status.
- Amendment/supersession relationships are linked or flagged unresolved.
- PDF page count matches the stored page records.
- Text/OCR extraction quality passes automated checks and manual sampling.
- Table extraction is sampled when tables are material.
- Redistribution/retention classification is recorded.

## Freshness

- Official source indexes are checked on a scheduled basis.
- A changed file at the same URL creates a new immutable document version.
- Checksums, not URLs, determine content identity.
- Newly discovered amendments enter quarantine until applicability is reviewed.
- Answers display the corpus freshness date and the as-of date used.
- A source freshness warning lowers confidence but does not automatically make an older rule invalid.

## Temporal applicability

Store publication and effective dates separately. When effective dates are ambiguous, the source is marked unresolved and cannot support an unconditional temporal claim.

Precedence is not derived from retrieval score. Authority, jurisdiction, effective period, and explicit amendment relationships are applied before semantic relevance.

## Page citations

Every PDF evidence citation records:

- stable source identifier;
- official document title and number;
- printed page number when reliably available;
- PDF page index;
- page range;
- text offsets or bounding boxes;
- canonical URL;
- document checksum.

When printed and PDF page numbers differ, the UI shows both. The system must not invent a page number for unpaginated HTML. HTML evidence is cited by URL, heading, and retrieval date and is labelled accordingly.

## Web fallback policy

Official web fallback may run when:

- the indexed corpus is older than its freshness threshold;
- a query cites a newer named document;
- retrieval strongly suggests a missing amendment;
- the source registry indicates incomplete coverage.

Fallback rules:

- Search only approved official domains.
- Never treat search-result snippets as final evidence.
- Open and verify the source document.
- Record retrieval time and checksum where downloadable.
- Label evidence as ephemeral until admitted through the source checklist.
- If authoritative support remains insufficient, abstain.

## Rights and redistribution

- Preserve source attribution and canonical links.
- Store only what is necessary for retrieval, verification, and audit.
- Do not redistribute access-controlled material.
- Use metadata-only indexing where redistribution rights are unclear.
- Honour removal or correction requirements while retaining an internal audit record where lawful.
- Never mix user-uploaded private documents into the public corpus.

## Corrections

Every answer should expose a correction-reporting route. A correction record includes the disputed claim, citation, proposed source, reviewer decision, and affected pipeline/corpus versions.
