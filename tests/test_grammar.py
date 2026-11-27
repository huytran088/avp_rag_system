"""The backend grammar must accept everything the AVP app's grammar does.

avp_rag/parser/Pseudocode.g4 is a copy of the app's
app/hooks/interpreter/Pseudocode.g4 (huytran088/algorithm-visualization-project),
the source of truth. These cases are features the old backend grammar lacked,
so a data file using them failed to ingest.
"""

import pytest
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from avp_rag import config
from avp_rag.ingest import parse_file
from avp_rag.parser import PseudocodeLexer, PseudocodeParser


class _Collect(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # noqa: N802
        self.errors.append(f"{line}:{column} {msg}")


def syntax_errors(source: str):
    listener = _Collect()
    lexer = PseudocodeLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)
    parser = PseudocodeParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    parser.program()
    return listener.errors


APP_FEATURES = {
    "not equal": "a = 1 != 2\n",
    "hash comment": "# a comment\nx = 1\n",
    "do-while": "i = 0\ndo:\n    i += 1\nwhile (i < 3)\n",
    "continue": "a = arr[1, 2]\nfor x in a:\n    continue\nend for\n",
    "elseif": "x = 1\nif (x == 1):\n    y = 1\nelseif (x == 2):\n    y = 2\nend if\n",
    "else if": "x = 1\nif (x == 1):\n    y = 1\nelse if (x == 2):\n    y = 2\nelse:\n    y = 3\nend if\n",
    "lowercase literals": "a = true\nb = false\nc = null\n",
    "empty array": "a = arr[]\n",
    "optional parentheses": "x = 1\nif x == 1:\n    y = 2\nend if\nwhile x < 3:\n    x += 1\nend while\n",
    "for-each parentheses": "a = arr[1, 2]\nfor (x in a):\n    y = x\nend for\n",
    "semicolons": "x = 1; y = 2\n",
    "chained directives": "a = arr[1, 2]\ni = 0\n@mark<i, outline, yellow> @log<info, \"hi\"> x = a[i]\n",
    "directive on return": "fun F(a):\n    @log<info, \"done\"> return a\nend fun\n",
    "multi-line array": "a = arr[\n    1,\n    2\n]\n",
}


@pytest.mark.parametrize("source", APP_FEATURES.values(), ids=APP_FEATURES.keys())
def test_parses_app_language_features(source):
    assert syntax_errors(source) == []


def test_rejects_what_the_app_rejects():
    # Array literals are only allowed on the right side of an assignment
    assert syntax_errors("result = Run(arr[3, 1, 2])\n") != []
    # Directive arguments can't be expressions
    assert syntax_errors("@mark<i + 1, outline> x = 1\n") != []


@pytest.mark.parametrize(
    "path",
    sorted(config.DATA_DIR.glob("*.avp")),
    ids=lambda p: p.name,
)
def test_data_files_parse_without_errors(path):
    assert syntax_errors(path.read_text()) == []


def test_parse_file_extracts_parameters_with_directives(tmp_path):
    path = tmp_path / "f.avp"
    path.write_text(
        "// Title\n\nfun Search(@init<table> array, @init<int> target):\n"
        "    do:\n        target -= 1\n    while (target > 0)\n    return array\nend fun\n"
    )
    (func,) = parse_file(path)
    assert func["name"] == "Search"
    assert func["parameters"] == ["array", "target"]
    assert func["code_content"].startswith("fun Search(")
    assert func["code_content"].endswith("end fun")
