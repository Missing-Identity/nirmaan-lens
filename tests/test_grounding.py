from nirmaan_lens.generation import validate_citations
from nirmaan_lens.models import Chunk


def evidence() -> list[Chunk]:
    return [
        Chunk(
            chunk_id="doc:p3:c1",
            source_id="DOC-1",
            document_title="Fixture",
            page_number=3,
            text="Evidence text",
            parent_id="doc:p3",
            authority="Fixture authority",
        )
    ]


def test_valid_citation_is_accepted() -> None:
    valid, errors = validate_citations("A supported claim. [DOC-1 p. 3]", evidence())
    assert valid
    assert errors == []


def test_fabricated_page_is_rejected() -> None:
    valid, errors = validate_citations("An unsupported claim. [DOC-1 p. 99]", evidence())
    assert not valid
    assert "not present" in errors[0]


def test_uncited_answer_is_rejected() -> None:
    valid, errors = validate_citations("An answer without evidence.", evidence())
    assert not valid
    assert errors == ["answer contains no citations"]
