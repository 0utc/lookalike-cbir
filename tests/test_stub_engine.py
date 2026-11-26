import pytest

from core import StubEngine


def test_results_sorted_and_limited():
    out = StubEngine(threshold=0.0).search(b"img", top_k=5)
    scores = [h.score for h in out.hits]
    assert len(out.hits) == 5 and scores == sorted(scores, reverse=True)


def test_same_image_same_results():
    e = StubEngine(threshold=0.0)
    assert e.search(b"abc") == e.search(b"abc")


def test_candidate_ids_restrict_results():
    out = StubEngine(threshold=0.0).search(b"img", candidate_ids=[3, 4, 5])
    assert {h.id for h in out.hits} == {3, 4, 5}


def test_no_relevant_result():
    out = StubEngine(threshold=0.99).search(b"img")
    assert out.no_relevant_result and out.hits == []


def test_add_remove_size():
    e = StubEngine(ids=[1, 2])
    e.add_or_update(3, b"x")
    e.remove(1)
    assert e.size() == 2


def test_unknown_model():
    with pytest.raises(ValueError):
        StubEngine().search(b"img", model="foo")