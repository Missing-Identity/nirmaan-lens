# ADR-004: Claim-Level Grounding, Clarification, and Abstention

- **Status:** Proposed
- **Date:** 2026-08-02

## Context

A confident but unsupported regulatory answer can cause costly decisions. Retrieval relevance alone does not prove that the final prose is supported.

## Decision

Require every material answer claim to reference one or more evidence passages and deterministic traces where applicable. Verify support, effective date, authority, and conflicts before release.

When required facts or support are insufficient, return a conditional answer, targeted clarification, source-conflict state, `not found`, or professional-review requirement.

Official-domain web fallback may be attempted for freshness gaps but cannot weaken the grounding policy.

## Consequences

- Some apparently helpful answers will be shorter or withheld.
- Citation precision and abstention quality become release metrics.
- Verification adds latency, which caching and staged checks must manage.
- The system must explain why it cannot answer.

## Rejected alternatives

- Attach citations only after generating free-form prose.
- Always answer with a general disclaimer.
- Use generic web search when the corpus is weak.
