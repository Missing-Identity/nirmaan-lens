# Product Scope

## Product statement

NirmaanLens is a Hyderabad-focused regulatory intelligence system that turns official development documents into page-cited answers and preliminary proposal checks.

The first release answers questions about building-permission pathways and core development constraints. It does not attempt comprehensive title due diligence, permit submission, or autonomous legal decision-making.

## Decision this project supports

Before paying for a detailed design or filing an application, a user should be able to decide:

- whether the proposal appears feasible under the indexed rules;
- which facts are still missing;
- which approvals and professional reviews may be required;
- which official clauses and amendments should be examined;
- whether a recent rule change affects the proposal.

## Primary persona

### Junior architect or civil engineer

**Context:** Works on small residential and mixed-use projects and repeatedly looks up rules while preparing early proposals.

**Jobs to be done:**

- Find the current clause without reading dozens of PDFs.
- Check whether a proposed height/use/plot combination triggers another pathway or NOC.
- Explain a constraint to a client with evidence.
- Compare an older interpretation with a recent amendment.

**Failure cost:** Rework, delayed submission, a misleading client commitment, or unnecessary consultant effort.

## Secondary personas

- Small builder assessing an opportunity before commissioning a full plan
- Homeowner trying to understand an architect's preliminary recommendation
- Permit consultant researching recent changes

## Core workflows

### Ask a rule

Input: Natural-language regulatory question, optional jurisdiction and as-of date.

Output: Direct answer, conditions, exceptions, applicable date, cited pages, source authority, and confidence.

### Check a proposal

Required facts are collected in a structured form:

- locality and competent authority;
- plot area and dimensions;
- abutting-road width;
- proposed use;
- proposed floors and/or height;
- relevant application date;
- optional overlay facts and documents.

Output: Preliminary constraints, approval path, deterministic calculations, assumptions, unresolved facts, and citations.

### Explain a regulatory change

Input: Topic, date range, or named government order.

Output: Before/after comparison, affected proposal types, unchanged provisions, uncertainty, and citations to both the base rule and amendment.

### Build an evidence packet

Output sections:

1. User-supplied facts
2. Jurisdiction and as-of date
3. Preliminary findings
4. Deterministic calculations
5. Applicable rules and exceptions
6. Missing evidence and conflicts
7. Page-level source appendix
8. Professional-review disclaimer

## MVP scope

The MVP will cover a deliberately narrow but deep slice:

- Core building-permission route selection
- Plot area, road width, proposed use, height, and basic setback-related questions
- Low-rise residential and small mixed-use proposals
- Selected high-rise trigger and Fire NOC questions
- Base Building Rules plus a curated amendment chain
- GHMC/HMDA-area material included only where authority and effective date are explicit

Final locality/jurisdiction boundaries will be frozen after domain interviews and corpus-access validation.

## Non-goals for the MVP

- Filing or tracking a permit application
- Certifying legality or approval probability
- Property-title, encumbrance, ownership-chain, or litigation verification
- Automatic interpretation of private sale deeds
- Generating architectural drawings
- Structural, fire, environmental, or aviation engineering certification
- State-wide Telangana coverage
- Fully automated geospatial boundary decisions from approximate coordinates
- Scraping authenticated, CAPTCHA-protected, or access-restricted portals

## Required answer states

The interface must support more than `yes` and `no`:

- **Supported:** evidence and required facts are sufficient for a preliminary answer.
- **Conditional:** answer changes based on one or more stated variables.
- **Clarification required:** a user fact such as road width or authority is missing.
- **Source conflict:** controlling documents appear inconsistent or the amendment chain is unresolved.
- **Not found:** the approved corpus and official fallback do not support an answer.
- **Professional review required:** the question exceeds the system's informational boundary.

## MVP success criteria

- At least five domain professionals agree to test the product.
- At least 100 real questions are collected before freezing the golden set.
- Hit Rate@10 reaches at least 0.90 on the reviewed MVP set.
- Citation precision reaches at least 0.95.
- Abstention F1 reaches at least 0.85 on negative/adversarial cases.
- No critical answer is released without a page-cited authoritative source.
- The benchmark shows the contribution of each retrieval stage.

## Signature demonstrations

1. Missing-road-width query produces a targeted clarification rather than a guessed height/setback answer.
2. A 2025-versus-2026 question retrieves and compares both rule versions.
3. A prompt referencing a nonexistent government order returns `not found`.
4. An instruction to ignore buffer-zone or safety rules is rejected as an attempt to override evidence policy.
