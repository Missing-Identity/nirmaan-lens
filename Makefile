.PHONY: setup demo run test eval doctor

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e ".[dev]"

demo:
	.venv/bin/nirmaan-lens bootstrap-demo
	.venv/bin/streamlit run app.py

run:
	.venv/bin/streamlit run app.py

test:
	.venv/bin/pytest

eval:
	.venv/bin/nirmaan-lens eval --provider local

doctor:
	.venv/bin/nirmaan-lens doctor

# Windows 11 is the primary platform. These targets remain for macOS/Linux contributors;
# the equivalent Windows entry point is `.\nirmaan.cmd <command>`.
