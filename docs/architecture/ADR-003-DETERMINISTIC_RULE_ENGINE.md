# ADR-003: Separate Deterministic Rules from Language Generation

- **Status:** Proposed
- **Date:** 2026-08-02

## Context

Plot feasibility involves unit conversion, threshold comparisons, lookup tables, and boundary conditions. Language models may explain these rules well but are unreliable as the sole calculator.

## Decision

Encode reviewed quantitative and decision-table rules in a versioned deterministic engine. Each rule must reference its source document, page, effective period, jurisdiction, reviewer state, and boundary tests.

The retrieval layer identifies evidence; the rule engine evaluates structured facts; the response composer explains the trace.

## Consequences

- Calculations become reproducible and testable.
- Rule encoding introduces a human-review cost.
- Some qualitative rules will remain RAG-only and must be labelled accordingly.
- A deterministic result cannot overrule a conflicting or missing authoritative source.

## Rejected alternatives

- Ask the LLM to calculate directly from retrieved tables.
- Build only a calculator with no documentary evidence.
- Encode all legal language as rules, which would create false precision and excessive maintenance.
