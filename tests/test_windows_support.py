from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_windows_launcher_routes_through_process_scoped_policy() -> None:
    launcher = (ROOT / "nirmaan.cmd").read_text(encoding="utf-8")
    assert "-ExecutionPolicy Bypass" in launcher
    assert "scripts\\nirmaan.ps1" in launcher


def test_windows_script_uses_windows_virtual_environment() -> None:
    script = (ROOT / "scripts" / "nirmaan.ps1").read_text(encoding="utf-8")
    assert '"Scripts\\python.exe"' in script
    assert '"-m", "nirmaan_lens"' in script
    assert '"-m", "streamlit"' in script


def test_windows_is_the_primary_documented_path() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    runbook = (ROOT / "docs" / "RUN_LOCAL.md").read_text(encoding="utf-8")
    assert "## Run it on Windows 11" in readme
    assert ".\\nirmaan.cmd setup" in readme
    assert runbook.startswith("# Windows-First Local Runbook")
