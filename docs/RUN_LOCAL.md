# Windows-First Local Runbook

## 1. Install the prerequisites

NirmaanLens targets 64-bit Windows 11 first. Install:

- Git for Windows;
- 64-bit Python 3.11 or newer from python.org;
- a modern browser.

In the Python installer, enable **Add python.exe to PATH**. The Python launcher (`py.exe`) is preferred when it is available.

Docker Desktop, WSL, Make, Visual Studio build tools, and an OpenAI API key are not required for the bundled demo.

## 2. Clone and set up

Open PowerShell or the PowerShell terminal in VS Code:

```powershell
git clone https://github.com/Missing-Identity/nirmaan-lens.git
cd nirmaan-lens
.\nirmaan.cmd setup
```

The setup command:

1. verifies Python 3.11+;
2. creates `.venv` with the Windows interpreter layout;
3. upgrades pip inside that environment;
4. installs the application and development dependencies.

You do not have to activate the virtual environment. The launcher always uses `.venv\Scripts\python.exe` directly, which avoids the most common PowerShell activation-policy problem.

## 3. Start the free demo

```powershell
.\nirmaan.cmd demo
```

Open the URL Streamlit prints, normally <http://localhost:8501>. Press `Ctrl+C` in PowerShell to stop it.

The demo installs the bundled synthetic fixture corpus and uses local BM25 plus deterministic feature-hash retrieval. It exercises the UI, hybrid ranking, citations, abstention, and evaluation mechanics without network calls or API charges. It is not a production semantic model or a source for real building decisions.

Try these prompts:

1. `When is a building treated as high-rise?`
2. `What information is needed to check setbacks?`
3. `Can I build inside a lake's full tank level?`
4. `Who won yesterday's cricket match?` — this should abstain.

## 4. Optional OpenAI mode

Create the ignored local configuration file:

```powershell
Copy-Item .env.example .env.local
notepad .env.local
```

Add the key and save:

```dotenv
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6-terra
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Then restart:

```powershell
.\nirmaan.cmd run
```

Select `openai` in the sidebar and enable grounded answer generation. Corpus embeddings are cached using the embedding model and the SHA-256 hash of each chunk, so unchanged text is not embedded again.

Never place a real key in a commit, issue, screenshot, or terminal command that will be shared. `.env.local` is ignored by Git.

## 5. Load official Telangana PDFs

Prove the download and parser path with one source first:

```powershell
.\nirmaan.cmd fetch-official --limit 1
.\nirmaan.cmd ingest-official
.\nirmaan.cmd doctor
.\nirmaan.cmd run
```

The first manifest entry is G.O.Ms.No.168. Parsed results preserve the PDF page number used by citations.

Fetch the complete starter manifest after the one-document path works:

```powershell
.\nirmaan.cmd fetch-official
.\nirmaan.cmd ingest-official
```

The ingestion report is written to `data\processed\ingestion_report.jsonl`. Scanned sources with too little embedded text are labelled `needs_ocr`; they are not silently treated as searchable.

Restore the synthetic demo at any time:

```powershell
.\nirmaan.cmd bootstrap-demo --force
```

## 6. Terminal and development commands

Ask a question without opening the UI:

```powershell
.\nirmaan.cmd ask "What height is defined as high-rise?" --provider local --no-generation
```

Run the checks used by Windows CI:

```powershell
.\nirmaan.cmd doctor
.\nirmaan.cmd check
.\nirmaan.cmd eval
```

`check` runs Ruff linting, Ruff formatting verification, and Pytest. `eval` runs the 60-case synthetic silver benchmark in offline mode.

Show every launcher command:

```powershell
.\nirmaan.cmd help
```

## 7. VS Code setup

After running setup:

1. Open the repository folder in VS Code.
2. Press `Ctrl+Shift+P`.
3. Choose **Python: Select Interpreter**.
4. Select `.venv\Scripts\python.exe`.
5. Use the integrated PowerShell terminal for `nirmaan.cmd` commands.

Activating `.venv` is optional. If you do activate it, PowerShell may ask about script execution policy; the checked-in `.cmd` launcher avoids that requirement and is the supported path.

## 8. Troubleshooting

### Python is not found

Close and reopen PowerShell after installing Python, then run:

```powershell
py -3 --version
python --version
```

At least one command must resolve to Python 3.11 or newer. If neither works, rerun the Python installer and enable **Add python.exe to PATH**.

### The virtual environment contains the wrong Python

The `.venv` directory is disposable and ignored by Git. Remove only that directory and repeat setup:

```powershell
Remove-Item -Recurse -Force .venv
.\nirmaan.cmd setup
```

### PowerShell blocks `.ps1` scripts

Use `.\nirmaan.cmd ...`, not the internal script directly. The launcher applies `ExecutionPolicy Bypass` only to its child process; it does not change the machine or user execution policy.

### Port 8501 is busy

```powershell
.\nirmaan.cmd run --server.port 8502
```

### The model call fails

Run `.\nirmaan.cmd doctor`, verify `openai_key_configured` is `true`, and try local mode. Retrieval and the evidence display remain usable without answer generation.

### A PDF reports `needs_ocr`

The source is likely scanned. OCR is a planned pipeline stage. Do not hand-label an empty parse as successful ingestion.

### Reset only the runtime corpus

```powershell
.\nirmaan.cmd bootstrap-demo --force
```

Runtime data, artifacts, caches, virtual environments, and secrets are ignored by Git.

## macOS/Linux contributor path

The code remains cross-platform. Contributors on macOS or Linux can use:

```bash
make setup
make demo
make test
make eval
```

Windows behavior is a release gate: the Windows launcher and benchmark run on `windows-latest` for every pull request and push to `main`.
