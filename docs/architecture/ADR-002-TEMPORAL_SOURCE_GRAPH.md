# ADR-002: Preserve a Temporal Source and Amendment Graph

- **Status:** Proposed
- **Date:** 2026-08-02

## Context

Building rules are amended, clarified, partially superseded, and applied differently across dates and jurisdictions. Destructively replacing old text prevents historical questions and makes provenance difficult to audit.

## Decision

Store every acquired document version immutably. Represent `amends`, `clarifies`, `supersedes`, and `effective-from/effective-to` relationships explicitly. Build a date-scoped effective view during query execution without deleting prior language.

## Consequences

- The system can answer before/after and as-of-date questions.
- Conflicting or incomplete amendment chains can be surfaced rather than hidden.
- Review effort increases because relationships may require expert confirmation.
- A source's publication date cannot be assumed to equal its effective date.

## Rejected alternatives

- Keep only the newest PDF: prevents historical reasoning and hides provenance.
- Merge amendments into a synthetic document only: useful as a convenience view but unacceptable as the sole source of truth.
- Let the language model infer precedence ad hoc: insufficiently reproducible.
