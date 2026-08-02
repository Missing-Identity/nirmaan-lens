[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$CommandArgs = @()
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvDirectory = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDirectory "Scripts\python.exe"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Executable"
    }
}

function Get-SystemPython {
    $Launcher = Get-Command "py.exe" -ErrorAction SilentlyContinue
    if ($null -ne $Launcher) {
        return @($Launcher.Source, "-3")
    }

    $Python = Get-Command "python.exe" -ErrorAction SilentlyContinue
    if ($null -ne $Python) {
        return @($Python.Source)
    }

    throw "Python was not found. Install Python 3.11+ from python.org and enable 'Add python.exe to PATH'."
}

function Invoke-SystemPython {
    param([string[]]$Arguments)

    $PythonCommand = Get-SystemPython
    $Executable = $PythonCommand[0]
    $Prefix = @()
    if ($PythonCommand.Count -gt 1) {
        $Prefix = $PythonCommand[1..($PythonCommand.Count - 1)]
    }
    Invoke-Checked -Executable $Executable -Arguments ($Prefix + $Arguments)
}

function Assert-Venv {
    if (-not (Test-Path $VenvPython)) {
        throw "The virtual environment is missing. Run '.\nirmaan.cmd setup' first."
    }
}

function Invoke-VenvPython {
    param([string[]]$Arguments)

    Assert-Venv
    Invoke-Checked -Executable $VenvPython -Arguments $Arguments
}

function Show-Help {
    @"
NirmaanLens Windows launcher

Usage:
  .\nirmaan.cmd setup                         Create .venv and install dependencies
  .\nirmaan.cmd demo                          Load the synthetic corpus and start the UI
  .\nirmaan.cmd run                           Start the UI with the active corpus
  .\nirmaan.cmd doctor                        Check Python, configuration, and corpus
  .\nirmaan.cmd test                          Run the test suite
  .\nirmaan.cmd eval                          Run the 60-case local benchmark
  .\nirmaan.cmd check                         Run lint, formatting checks, and tests
  .\nirmaan.cmd fetch-official --limit 1      Download official PDFs
  .\nirmaan.cmd ingest-official               Build page-aware chunks from downloaded PDFs
  .\nirmaan.cmd bootstrap-demo --force        Restore the synthetic corpus
  .\nirmaan.cmd ask "What is an OC?" --provider local --no-generation

Python 3.11 or newer is required. The demo and local evaluation do not require an API key.
"@ | Write-Host
}

Push-Location $ProjectRoot
try {
    switch ($Command.ToLowerInvariant()) {
        "setup" {
            Invoke-SystemPython -Arguments @(
                "-c",
                "import sys; print('Python', sys.version.split()[0]); sys.exit(0 if sys.version_info >= (3, 11) else 1)"
            )
            if (-not (Test-Path $VenvPython)) {
                Invoke-SystemPython -Arguments @("-m", "venv", $VenvDirectory)
            }
            Invoke-VenvPython -Arguments @("-m", "pip", "install", "--upgrade", "pip")
            Invoke-VenvPython -Arguments @("-m", "pip", "install", "-e", ".[dev]")
            Write-Host "Setup complete. Run '.\nirmaan.cmd demo'." -ForegroundColor Green
        }
        "demo" {
            Invoke-VenvPython -Arguments @("-m", "nirmaan_lens", "bootstrap-demo")
            Invoke-VenvPython -Arguments @("-m", "streamlit", "run", "app.py")
        }
        "run" {
            Invoke-VenvPython -Arguments (@("-m", "streamlit", "run", "app.py") + $CommandArgs)
        }
        "doctor" {
            Invoke-VenvPython -Arguments @("-m", "nirmaan_lens", "doctor")
        }
        "test" {
            $env:NIRMAAN_OFFLINE = "1"
            Invoke-VenvPython -Arguments (@("-m", "pytest") + $CommandArgs)
        }
        "eval" {
            $env:NIRMAAN_OFFLINE = "1"
            Invoke-VenvPython -Arguments @("-m", "nirmaan_lens", "eval", "--provider", "local")
        }
        "lint" {
            Invoke-VenvPython -Arguments @("-m", "ruff", "check", ".")
        }
        "format-check" {
            Invoke-VenvPython -Arguments @("-m", "ruff", "format", "--check", ".")
        }
        "check" {
            $env:NIRMAAN_OFFLINE = "1"
            Invoke-VenvPython -Arguments @("-m", "ruff", "check", ".")
            Invoke-VenvPython -Arguments @("-m", "ruff", "format", "--check", ".")
            Invoke-VenvPython -Arguments @("-m", "pytest")
        }
        "fetch-official" {
            Invoke-VenvPython -Arguments (@("-m", "nirmaan_lens", "fetch-official") + $CommandArgs)
        }
        "ingest-official" {
            Invoke-VenvPython -Arguments @("-m", "nirmaan_lens", "ingest-official")
        }
        "bootstrap-demo" {
            Invoke-VenvPython -Arguments (@("-m", "nirmaan_lens", "bootstrap-demo") + $CommandArgs)
        }
        "ask" {
            Invoke-VenvPython -Arguments (@("-m", "nirmaan_lens", "ask") + $CommandArgs)
        }
        { $_ -in @("help", "-h", "--help", "/?") } {
            Show-Help
        }
        default {
            Show-Help
            throw "Unknown command: $Command"
        }
    }
}
finally {
    Pop-Location
}
