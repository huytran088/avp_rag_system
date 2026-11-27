"""Metric math for the retrieval eval (evals/retrieval_eval.py)."""

import pytest

from evals.retrieval_eval import mrr, recall_at_k, summarize


def test_recall_at_k_counts_any_expected_in_top_k():
    ranked = ["A", "B", "C"]
    assert recall_at_k(ranked, {"B"}, 1) == 0.0
    assert recall_at_k(ranked, {"B"}, 2) == 1.0
    # Half of the expected functions are in the top 2
    assert recall_at_k(ranked, {"A", "C"}, 2) == 0.5


def test_mrr_uses_first_expected_hit():
    assert mrr(["A", "B", "C"], {"C"}) == pytest.approx(1 / 3)
    assert mrr(["A", "B"], {"A", "B"}) == 1.0
    assert mrr(["A", "B"], {"Z"}) == 0.0


def test_summarize_skips_coverage_gaps():
    rows = [
        {"id": "t1", "expected": ["A"], "ranked": ["A", "B"]},
        {"id": "t2", "expected": ["B"], "ranked": ["A", "B"]},
        {"id": "gap", "expected": [], "ranked": ["A", "B"]},
    ]
    s = summarize(rows, ks=(1, 2))
    assert s["labeled"] == 2
    assert s["gaps"] == ["gap"]
    assert s["recall@1"] == 0.5
    assert s["recall@2"] == 1.0
    assert s["mrr"] == pytest.approx(0.75)
