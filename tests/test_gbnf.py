"""evals/avp.gbnf, the grammar for the constrained-decoding experiment.

Uses xgrammar's testing helper (eval dependency group):
uv run --group eval pytest tests/test_gbnf.py
"""

from pathlib import Path

import pytest

from avp_rag import config

xgr_testing = pytest.importorskip("xgrammar.testing")

GRAMMAR = (Path(__file__).parents[1] / "evals" / "avp.gbnf").read_text()
DATA = sorted(config.DATA_DIR.glob("*.avp"))


def accepts(source: str) -> bool:
    return xgr_testing._is_grammar_accept_string(GRAMMAR, source)


@pytest.mark.parametrize("path", DATA, ids=lambda p: p.name)
def test_accepts_every_data_file(path):
    # Bytes as they are: CRLF line endings must be accepted too
    assert accepts(path.read_bytes().decode("utf-8"))


def test_accepts_the_tutor_example_shapes():
    source = """// Example
a1 = arr[5, 1, 4]
b = arr[]
c = arr(3, 0)
d = arr[1 to 5]

fun Sort(@init<table> array, low, high):
    for @mark<j, outline, yellow> (j = low; j < high; j += 1):
        if (array[j] > array[j + 1]):
            swap(array[j], array[j + 1])
        else if array[j] == 0:
            continue
        else:
            @log<info, "ok"> k = -j ** 2 % 3
        end if
    end for
    do:
        low += 1
    while (low < high and not_done != 0)
    for x in array:
        break
    end for
    return array
end fun

result = Sort(a1, 0, length(a1) - 1)
"""
    assert accepts(source)


@pytest.mark.parametrize(
    "source",
    [
        "x = [1, 2]\n",  # bare list literal
        "fun F(a):\n    return a\n",  # missing end fun
        "@mark<i + 1> x = 1\n",  # expression as a directive argument
        "x = arr[1, 2]\ny = arr[1, 2][0]\n",  # indexing a literal
        "x++\n",
        "x *= 2\n",
        "fun F(a):\n    return a\nendfun\n",
    ],
)
def test_rejects_what_the_app_rejects(source):
    assert not accepts(source)
