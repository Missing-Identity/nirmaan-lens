# Contributing

NirmaanLens is in a documentation-first architecture phase. Early contributions should improve product scope, source provenance, evaluation quality, or architecture decisions before adding broad implementation code.

## Good first contributions

- Identify an official source missing from the manifest.
- Propose a real, de-identified user question for review.
- Find an amendment relationship or effective-date ambiguity.
- Improve the error taxonomy or adversarial suite.
- Review chunking behavior on a difficult table or scanned page.
- Challenge an architecture decision with measurable alternatives.

## Source contributions

Provide:

- official canonical URL;
- issuing authority;
- document title and number;
- publication and effective dates if known;
- jurisdiction and affected topics;
- relationship to existing rules;
- access or redistribution concerns;
- pages relevant to the proposed use case.

Do not submit downloaded restricted documents or bypass portal controls.

## Evaluation contributions

Do not place private personal/property information in public issues or fixtures. Questions should be de-identified or synthetic while preserving the regulatory reasoning being tested.

A proposed golden case must specify the expected answer state and authoritative evidence. Model-generated answer keys are not accepted without human review.

## Decision process

Material technical choices are documented as Architecture Decision Records in `docs/architecture/`. Proposed decisions remain replaceable until corpus or evaluation evidence supports acceptance.

## Development workflow

Once implementation begins:

1. Open or select an issue with acceptance criteria.
2. Create a focused branch.
3. Keep unrelated changes separate.
4. Add tests and evaluation cases for behavior changes.
5. Record model, corpus, and configuration versions for retrieval experiments.
6. Submit a pull request explaining the measured impact and limitations.

## Safety

Do not present test outputs as building approval, legal advice, or professional certification. Report security issues privately as described in `SECURITY.md`.
