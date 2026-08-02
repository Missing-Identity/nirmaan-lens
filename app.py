from __future__ import annotations

import json

import streamlit as st

from nirmaan_lens.config import Settings
from nirmaan_lens.corpus import bootstrap_demo, corpus_summary
from nirmaan_lens.evaluation import run_benchmark
from nirmaan_lens.io import load_chunks
from nirmaan_lens.service import NirmaanLensService

st.set_page_config(page_title="NirmaanLens Hyderabad", page_icon="🏗️", layout="wide")
settings = Settings()
settings.ensure_runtime_dirs()
chunks = load_chunks(settings.chunk_path) or bootstrap_demo(settings)
summary = corpus_summary(chunks)


@st.cache_resource(show_spinner="Building the hybrid index…")
def get_service(corpus_stamp: float, provider: str, generation: bool) -> NirmaanLensService:
    del corpus_stamp
    current_chunks = load_chunks(settings.chunk_path) or bootstrap_demo(settings)
    return NirmaanLensService(
        current_chunks,
        settings,
        embedding_provider=provider,
        use_generation=generation,
    )


st.title("NirmaanLens Hyderabad")
st.caption("Source-grounded building-rule research with page citations and measurable retrieval")

if summary["kinds"] == ["synthetic"]:
    st.warning(
        "Demo corpus active. Its fixtures are synthetic and are only for testing retrieval, "
        "citations, abstention, and the UI—not for making a real building decision."
    )
else:
    st.info(
        "Official PDF corpus active. Results are preliminary research, not an approval or opinion."
    )

with st.sidebar:
    st.header("Retrieval controls")
    provider_options = ["local"] + (["openai"] if settings.openai_api_key else [])
    provider = st.selectbox(
        "Embedding provider",
        provider_options,
        help="Local is deterministic and free. OpenAI is semantic and cached by content hash.",
    )
    generation = st.toggle(
        "Generate a grounded answer",
        value=bool(settings.openai_api_key),
        disabled=not settings.openai_api_key,
    )
    authorities = sorted({chunk.authority for chunk in chunks})
    topics = sorted({topic for chunk in chunks for topic in chunk.topics})
    authority_choice = st.selectbox("Authority filter", ["All", *authorities])
    topic_choice = st.selectbox("Topic filter", ["All", *topics])
    st.divider()
    st.metric("Sources", summary["sources"])
    st.metric("Page-aware chunks", summary["chunks"])
    st.caption(f"Answer model: `{settings.answer_model}`")

ask_tab, lab_tab, eval_tab, sources_tab = st.tabs(["Ask", "Retrieval lab", "Evaluation", "Sources"])

samples = [
    "When is a building treated as high-rise?",
    "What information is needed to check setbacks?",
    "Can I build inside a lake's full tank level?",
    "Does the system guarantee my building approval?",
]

with ask_tab:
    selected_sample = st.selectbox("Try an example", ["Write my own question", *samples])
    default_question = "" if selected_sample == "Write my own question" else selected_sample
    question = st.text_area(
        "Question",
        value=default_question,
        placeholder="Example: Is an 18 metre building considered high-rise?",
        height=100,
    )
    if st.button("Find grounded evidence", type="primary", disabled=not question.strip()):
        stamp = settings.chunk_path.stat().st_mtime
        try:
            service = get_service(stamp, provider, generation)
            with st.spinner("Running sparse + dense retrieval and checking citations…"):
                response = service.answer(
                    question.strip(),
                    authority=None if authority_choice == "All" else authority_choice,
                    topic=None if topic_choice == "All" else topic_choice,
                )
            state_col, confidence_col, provider_col = st.columns(3)
            state_col.metric("Answer state", response.answer_state)
            confidence_col.metric("Retrieval confidence", f"{response.confidence:.0%}")
            provider_col.metric("Embedding", response.provider)
            for warning in response.warnings:
                st.warning(warning)
            st.markdown(response.answer)
            st.subheader("Evidence trail")
            for result in response.results[:5]:
                label = f"#{result.rank} {result.chunk.document_title} — {result.chunk.citation}"
                with st.expander(label, expanded=result.rank == 1):
                    st.write(result.chunk.text)
                    metric_cols = st.columns(3)
                    metric_cols[0].metric("Sparse", f"{result.sparse_score:.3f}")
                    metric_cols[1].metric("Dense", f"{result.dense_score:.3f}")
                    metric_cols[2].metric("RRF", f"{result.score:.4f}")
                    if result.chunk.source_url:
                        st.link_button("Open source", result.chunk.source_url)
        # Keep the interactive app alive while exposing the actionable runtime failure.
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not run the query: {type(exc).__name__}: {exc}")

with lab_tab:
    st.subheader("What the current query path does")
    st.markdown(
        "1. Normalizes aliases and expands domain terms.\n"
        "2. Applies authority/topic metadata filters.\n"
        "3. Runs BM25 and dense retrieval independently.\n"
        "4. Fuses ranks using reciprocal-rank fusion.\n"
        "5. Pulls sibling chunks from each top result's parent page.\n"
        "6. Generates only from evidence and validates every source/page citation.\n"
        "7. Abstains when retrieval confidence is below the gate."
    )
    st.caption(
        "Cross-encoder reranking, ColBERT late interaction, temporal source graphs, and official "
        "web fallback are intentionally tracked as later benchmarked stages."
    )

with eval_tab:
    st.subheader("Retrieval quality dashboard")
    st.write(
        "The bundled suite contains 60 synthetic silver cases. It is useful for regression testing, "
        "but it becomes a true golden set only after independent source/page review."
    )
    if st.button("Run 60-case local benchmark"):
        with st.spinner("Comparing naive dense top-5 with hybrid top-10…"):
            report = run_benchmark(chunks, settings, provider="local")
        st.session_state["eval_report"] = report
    report = st.session_state.get("eval_report")
    latest_path = settings.artifact_dir / "eval-latest.json"
    if report is None and latest_path.exists():
        report = json.loads(latest_path.read_text(encoding="utf-8"))
    if report:
        baseline = report["baseline"]
        hybrid = report["hybrid"]
        metric_cols = st.columns(4)
        metric_cols[0].metric(
            "Hit Rate",
            f"{hybrid['hit_rate']:.1%}",
            f"{report['improvement']['hit_rate']:+.1%}",
        )
        metric_cols[1].metric(
            "MRR",
            f"{hybrid['mrr']:.3f}",
            f"{report['improvement']['mrr']:+.3f}",
        )
        metric_cols[2].metric(
            "NDCG",
            f"{hybrid['ndcg']:.3f}",
            f"{report['improvement']['ndcg']:+.3f}",
        )
        metric_cols[3].metric("Abstention F1", f"{hybrid['abstention_f1']:.3f}")
        st.dataframe(
            [
                {
                    "Pipeline": "Naive dense top-5",
                    "Hit Rate": baseline["hit_rate"],
                    "MRR": baseline["mrr"],
                    "NDCG": baseline["ndcg"],
                    "ms/query": baseline["milliseconds_per_query"],
                },
                {
                    "Pipeline": "Hybrid top-10",
                    "Hit Rate": hybrid["hit_rate"],
                    "MRR": hybrid["mrr"],
                    "NDCG": hybrid["ndcg"],
                    "ms/query": hybrid["milliseconds_per_query"],
                },
            ],
            use_container_width=True,
            hide_index=True,
        )

with sources_tab:
    st.subheader("Active corpus")
    source_rows = {}
    for chunk in chunks:
        source_rows[chunk.source_id] = {
            "Source ID": chunk.source_id,
            "Title": chunk.document_title,
            "Authority": chunk.authority,
            "Kind": chunk.source_kind,
            "URL": chunk.source_url,
        }
    st.dataframe(list(source_rows.values()), use_container_width=True, hide_index=True)
    st.code(
        ".venv/bin/nirmaan-lens fetch-official\n"
        ".venv/bin/nirmaan-lens ingest-official\n"
        ".venv/bin/streamlit run app.py",
        language="bash",
    )

st.divider()
st.caption(
    "Preliminary informational research only. Not a government approval, legal opinion, "
    "architectural certification, title report, or substitute for a licensed professional."
)
