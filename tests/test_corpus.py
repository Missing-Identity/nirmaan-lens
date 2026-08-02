from nirmaan_lens.corpus import chunk_text


def test_chunking_enforces_minimum_contract() -> None:
    text = " ".join(f"token-{index}" for index in range(1600))
    chunks = chunk_text(text, chunk_tokens=550, overlap_tokens=75)
    assert len(chunks) >= 3
    assert all(token_count <= 550 for _, token_count in chunks)
    assert chunks[0][1] == 550


def test_chunking_rejects_too_small_windows() -> None:
    try:
        chunk_text("example", chunk_tokens=499, overlap_tokens=75)
    except ValueError as exc:
        assert "at least 500" in str(exc)
    else:
        raise AssertionError("expected the minimum chunk-size contract to be enforced")


def test_chunking_rejects_too_small_overlap() -> None:
    try:
        chunk_text("example", chunk_tokens=550, overlap_tokens=49)
    except ValueError as exc:
        assert "at least 50" in str(exc)
    else:
        raise AssertionError("expected the minimum overlap contract to be enforced")
