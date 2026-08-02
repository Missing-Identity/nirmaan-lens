# Threat Model and Safety Controls

## Protected outcomes

- Users must not mistake a preliminary answer for a permit, certification, or legal opinion.
- Material claims must remain tied to authentic, applicable sources.
- Private user documents must not leak into the public corpus or another user's session.
- Source documents and web pages must not be able to override system policy.
- Attackers must not silently poison the shared corpus.

## Trust boundaries

| Boundary | Untrusted input |
|---|---|
| User interface | Questions, structured facts, uploaded documents |
| Acquisition | Remote PDFs, HTML, redirects, changed files |
| Parsing/OCR | Extracted text, tables, hidden text layers |
| Retrieval | Semantically relevant but inapplicable or malicious passages |
| Web fallback | Search results, snippets, unofficial mirrors |
| Generation | Model output and unsupported synthesis |

## Principal threats

### Prompt injection in sources

A PDF or webpage may contain instructions aimed at the model.

Controls:

- Treat source text exclusively as evidence.
- Never expose tool or policy control to retrieved content.
- Strip active content and do not execute embedded scripts/macros.
- Include injection examples in the adversarial suite.

### Corpus poisoning

An unofficial, modified, or replaced document could enter the index.

Controls:

- Official-domain allowlist and canonical-source verification.
- Immutable files and checksums.
- Quarantine new or changed documents.
- Manual sampling and amendment-link review.
- Source authority is separate from retrieval score.

### Temporal or jurisdiction mismatch

A relevant passage may not apply to the requested date or location.

Controls:

- Required effective-date and jurisdiction metadata.
- Filter before reranking where applicability is known.
- Explicit unresolved state when applicability cannot be established.
- Temporal test slice and before/after cases.

### Citation laundering

A citation may be real while failing to support the generated claim.

Controls:

- Claim-level support verification.
- Page and bounding-box evidence preview.
- Citation precision as a release gate.
- Remove or qualify claims that fail entailment review.

### Unsafe overconfidence

The system may sound definitive despite missing facts or incomplete coverage.

Controls:

- Required-field validation.
- Multi-state answer contract: supported, conditional, clarification, conflict, not found, professional review.
- Plain-language confidence factors rather than a decorative score.
- No approval-probability claim in the MVP.

### Calculation manipulation or error

Users may provide inconsistent units or boundary values; an LLM may miscalculate.

Controls:

- Normalize units explicitly and display conversions.
- Run reviewed calculations in a deterministic engine.
- Test every encoded boundary below, at, and above its threshold.
- Preserve the rule and calculation trace.

### Private-document leakage

Controls:

- Tenant-isolated storage and indexes.
- No public-corpus promotion.
- Defined retention and deletion controls before accepting sensitive uploads.
- Redact direct identifiers from evaluation and observability traces.
- Do not use private uploads for model training by default.

### Denial of service and cost abuse

Controls:

- Upload size/page limits.
- Rate and concurrency limits.
- Bounded candidate pools and generation context.
- Cache and deduplicate document embeddings.
- Require explicit workflows for large batch ingestion.

## User-visible safeguards

- Always display the as-of date and authority assumption.
- Separate user facts, calculated results, and official evidence.
- Make cited pages inspectable.
- Explain missing facts and source conflicts.
- State that the output is preliminary informational analysis.
- Recommend licensed professional review for material decisions.

## Out of scope for the MVP threat model

- Permit-submission credentials
- Payment processing
- Government-portal account automation
- Digital signatures
- Binding professional certifications

These features require a new security review before implementation.
