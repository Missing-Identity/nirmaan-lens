# Local Runbook

## Fastest path on a MacBook

Open Terminal (or the terminal inside VS Code) and run:

```bash
git clone https://github.com/Missing-Identity/nirmaan-lens.git
cd nirmaan-lens
python3 --version
make setup
make demo
```

Python must be 3.11 or newer. On a fresh Mac, install command-line developer tools if Git or Make is missing:

```bash
xcode-select --install
```

If the system Python is too old, install a current Python from Homebrew or python.org, then rerun `make setup`.

Streamlit prints a local URL, normally `http://localhost:8501`. Press `Control-C` in the terminal to stop it.

## Zero-cost mode

`make demo` installs the synthetic fixture corpus and starts the app. The local provider combines BM25 with deterministic feature hashing. It is useful for UI work, tests, evaluation mechanics, and offline development; it is not a production semantic embedding model.

No API key is needed. In the sidebar:

1. Select `local` as the embedding provider.
2. Leave grounded answer generation disabled.
3. Try “When is a building treated as high-rise?”
4. Inspect sparse, dense, and fused scores in the evidence trail.
5. Open Evaluation and run the 60-case benchmark.

## OpenAI semantic mode

Create a local environment file:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```dotenv
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6-terra
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

The key file is ignored by Git. Never paste a real key into an issue, commit, screenshot, or chat log.

Restart the app with `make run`, select `openai`, and enable grounded answer generation. Corpus embeddings are cached by the embedding model plus the SHA-256 hash of each chunk, so unchanged text is not embedded again.

## Official PDF mode

The source manifest contains verified government or government-catalogued URLs. Start with one source:

```bash
.venv/bin/nirmaan-lens fetch-official --limit 1
.venv/bin/nirmaan-lens ingest-official
.venv/bin/nirmaan-lens doctor
.venv/bin/streamlit run app.py
```

That first document is G.O.Ms.No.168. In the current parser smoke test it produces hundreds of page-aware chunks and retains PDF page numbers in each result.

Fetch all starter sources when the one-document path works:

```bash
.venv/bin/nirmaan-lens fetch-official
.venv/bin/nirmaan-lens ingest-official
```

The ingestion report is written to `data/processed/ingestion_report.jsonl`. Scanned sources with too little embedded text are labeled `needs_ocr`; they are not silently treated as searchable.

To return to the bundled fixture corpus:

```bash
.venv/bin/nirmaan-lens bootstrap-demo --force
```

## Terminal-only use

```bash
.venv/bin/nirmaan-lens ask "What height is defined as high-rise?" \
  --provider local --no-generation
```

Remove `--no-generation` and use `--provider openai` for a grounded generated response.

## Validation

```bash
make doctor
make test
make eval
```

Expected v0.1 checks:

- 13 tests pass;
- the evaluation suite reports 60 cases;
- the active demo corpus reports 16 chunks, 15 pages, and 5 synthetic sources;
- the synthetic hybrid benchmark reports Hit Rate, MRR, NDCG, and abstention metrics.

## Common problems

### `python3` is too old

Install Python 3.11+ and delete `.venv`, then rerun `make setup`. Deleting `.venv` only removes the reproducible local environment; it does not remove source code or datasets.

### Port 8501 is busy

```bash
.venv/bin/streamlit run app.py --server.port 8502
```

### The model call fails

Run `make doctor`, verify that `openai_key_configured` is `true`, and try local mode. Retrieval and evidence display remain usable without generation.

### A PDF reports `needs_ocr`

The source is likely scanned. OCR is a planned pipeline stage. Do not hand-label an empty parse as a successful ingestion.

### Reset only the runtime corpus

```bash
.venv/bin/nirmaan-lens bootstrap-demo --force
```

Runtime data, artifacts, caches, and secrets are ignored by Git.

