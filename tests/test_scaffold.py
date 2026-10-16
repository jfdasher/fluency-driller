from drill.content.scaffold import scaffold


def test_scaffold_comments_prompt_then_stub():
    out = scaffold("Return x.", "def solve(d):\n    ...", "solve")
    assert out == "# Return x.\ndef solve(d):\n    ..."


def test_scaffold_multiline_prompt_each_line_commented():
    out = scaffold("line one\nline two", "def solve():\n    ...", "solve")
    assert out.startswith("# line one\n# line two\n")


def test_scaffold_falls_back_to_entry_point_when_no_stub():
    out = scaffold("P", None, "myfunc")
    assert out == "# P\ndef myfunc(...):\n    ..."
