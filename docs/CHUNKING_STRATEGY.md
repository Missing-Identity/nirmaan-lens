# Chunking Strategy

## Current contract

- Parse PDFs one page at a time.
- Normalize whitespace and repair line-break hyphenation.
- Encode with `o200k_base`.
- Create 550-token child chunks.
- Reuse 75 tokens between adjacent children.
- Keep each child inside one PDF page.
- Store PDF page number, optional printed page, source, authority, topics, jurisdictions, effective dates, and parent page ID on every chunk.
- Retrieve child chunks and expand the parents of the top results before generation.

The implementation rejects a configuration below 500 tokens or 50 tokens of overlap.

## Why 550/75 is the starting point

Building rules contain definitions, exceptions, provisos, and tables whose meaning often spans several sentences. Very small chunks separate a threshold from its exception. Very large chunks dilute retrieval and increase reranking and generation cost. A 550-token window is large enough for a typical clause neighborhood while remaining focused; a 75-token overlap keeps page-local transitions and trailing provisos discoverable.

Page boundaries are a hard constraint because a page citation must be mechanically traceable. A child never claims one page while containing text from another.

## Parent retrieval

The current parent is the PDF page. After ranking child chunks, the service adds sibling chunks from the same top parent pages, capped at eight evidence chunks. This gives generation more local context without widening the initial search query.

The next parser will add section-level parents above pages. Those parents may span pages, but every sentence-level evidence span will retain its page mapping.

## Tables and scans

Plain PDF text extraction is insufficient for scanned rules and complex tables. Pages with fewer than 80 normalized characters are excluded and reported for OCR. This prevents an empty or garbled page from appearing successfully indexed.

The planned parser benchmark compares native text extraction, layout-aware extraction, and OCR on:

- exact text recovery;
- page and printed-page mapping;
- table cell order;
- header/footer removal;
- clause boundary preservation;
- retrieval performance on OCR/table cases.

## How the choice will be validated

The project will ablate at least:

- 500/50;
- 550/75;
- 700/100;
- layout-aware section chunks;
- child-only versus child-plus-parent retrieval.

The selected strategy must improve official-document Hit Rate, MRR, NDCG, and citation accuracy without an unacceptable p95 latency or context-cost increase. The current setting is a tested implementation default, not a universal claim.

