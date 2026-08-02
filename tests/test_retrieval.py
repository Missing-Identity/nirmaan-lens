from pathlib import Path

from nirmaan_lens.io import load_chunks
from nirmaan_lens.retrieval import HybridRetriever, LocalHashEmbedder, rewrite_and_expand

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = load_chunks(ROOT / "fixtures" / "demo_corpus.jsonl")


def test_query_expansion_maps_oc() -> None:
    assert "occupancy certificate" in rewrite_and_expand("Do I need an OC?")


def test_hybrid_retrieval_finds_high_rise_boundary() -> None:
    retriever = HybridRetriever(CHUNKS, LocalHashEmbedder())
    bundle = retriever.search("Is 18 metres a high-rise boundary?", top_k=10)
    assert bundle.results[0].chunk.chunk_id == "DEMO-BR:p2:c1"
    assert bundle.confidence > 0.24


def test_metadata_filter_scopes_results() -> None:
    retriever = HybridRetriever(CHUNKS, LocalHashEmbedder())
    bundle = retriever.search("What depends on height?", topic="fire-noc")
    assert bundle.results
    assert all("fire-noc" in result.chunk.topics for result in bundle.results)


def test_unrelated_query_has_low_confidence() -> None:
    retriever = HybridRetriever(CHUNKS, LocalHashEmbedder())
    bundle = retriever.search("Who won yesterday's international cricket match?")
    assert bundle.confidence < 0.24
