"""Retrieval eval: recall@k and MRR on labeled requests, reranker on and off.

Usage: uv run python -m evals.retrieval_eval [--labels evals/retrieval_labels.json]

Requests whose label lists no function have no example in data/*.avp. They
are reported as coverage gaps instead of counting as misses.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

LABELS = Path(__file__).with_name("retrieval_labels.json")
KS = (1, 2, 5)


def recall_at_k(ranked: Sequence[str], expected: Set[str], k: int) -> float:
    """Share of the expected functions found in the top k."""
    return len(expected & set(ranked[:k])) / len(expected)


def mrr(ranked: Sequence[str], expected: Set[str]) -> float:
    """Reciprocal rank of the first expected function (0 when none is found)."""
    for i, name in enumerate(ranked, start=1):
        if name in expected:
            return 1 / i
    return 0.0


def summarize(rows: List[Dict], ks: Iterable[int] = KS) -> Dict:
    labeled = [r for r in rows if r["expected"]]
    out: Dict = {
        "labeled": len(labeled),
        "gaps": [r["id"] for r in rows if not r["expected"]],
    }
    n = len(labeled) or 1
    for k in ks:
        out[f"recall@{k}"] = sum(recall_at_k(r["ranked"], set(r["expected"]), k) for r in labeled) / n
    out["mrr"] = sum(mrr(r["ranked"], set(r["expected"])) for r in labeled) / n
    out["misses@2"] = [
        {"id": r["id"], "expected": r["expected"], "top2": r["ranked"][:2]}
        for r in labeled
        if recall_at_k(r["ranked"], set(r["expected"]), 2) < 1
    ]
    return out


def run(labels_path: Path = LABELS) -> Dict:
    from avp_rag.retrieve import get_retriever

    labels = json.loads(labels_path.read_text())
    retriever = get_retriever()
    k = max(KS)
    report = {}
    for rerank in (True, False):
        retriever.use_reranker = rerank
        rows = [
            {
                "id": item["id"],
                "expected": item["expected"],
                "ranked": [r["function_name"] for r in retriever.retrieve(item["query"], k=k)],
            }
            for item in labels
        ]
        report["rerank" if rerank else "no_rerank"] = summarize(rows)
    retriever.use_reranker = True
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", type=Path, default=LABELS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run(args.labels)
    text = json.dumps(report, indent=2)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
