from pathlib import Path

from nirmaan_lens.config import Settings
from nirmaan_lens.evaluation import run_benchmark
from nirmaan_lens.io import load_chunks, read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_silver_suite_contains_sixty_cases(tmp_path: Path) -> None:
    cases = read_jsonl(ROOT / "evals" / "silver_v0.1.jsonl")
    assert len(cases) == 60
    assert sum(case["expected_answer_state"] == "not_found" for case in cases) == 10


def test_benchmark_reports_required_metrics(tmp_path: Path) -> None:
    settings = Settings(artifact_dir=tmp_path)
    chunks = load_chunks(ROOT / "fixtures" / "demo_corpus.jsonl")
    report = run_benchmark(chunks, settings, provider="local")
    assert report["hybrid"]["case_count"] == 60
    assert {"hit_rate", "mrr", "ndcg"} <= report["hybrid"].keys()
    assert (tmp_path / "eval-latest.json").exists()
