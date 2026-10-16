"""Per-corpus authoring profiles for the content generator.

The generator composes its system prompt as CORE_SYSTEM_PROMPT (corpus-agnostic,
in generator.py) + the corpus's `system_section`. Keyed on CORPUS, because pandas
and python both run under grader `python` at runtime — the difference is purely an
authoring concern (imports, equality style, prompt formatting).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorpusProfile:
    name: str
    system_section: str


# The Python examples embed literal backslash-n (\\n) so the model sees the JSON
# escaping it must reproduce — matching the legacy _SYSTEM_PROMPT verbatim.
_PYTHON_SECTION = (
    "You write atomic Python drill questions that target ONE idiom each. "
    "Tests may also use `equal(a, b)` (tuple/list-tolerant equality), injected "
    "alongside `fn`. Examples: for a factory, "
    "{name: 'test_basic', source: 'def test_basic():\\n    assert make_multiplier(3)(5) == 15'}; "
    "for deep-copy independence, "
    "{name: 'test_independent', source: 'def test_independent():\\n    g = [[0,0],[0,0]]\\n    c = deep_copy(g)\\n    c[0][0] = 9\\n    assert g[0][0] == 0'}."
)

_PANDAS_SECTION = """\
You write atomic pandas drill questions (pandas 2.x, numpy-backed) that target ONE \
idiom each. The entry_point receives real pandas objects and must return a NEW \
object without mutating its inputs. The canonical_answer and every test may \
`import pandas as pd` and `import numpy as np`.

TEST CONTRACT (hybrid): give each question exactly ONE exact-equality test plus one \
or two targeted edge tests.
- The exact test builds the expected object explicitly and compares with \
`from pandas.testing import assert_frame_equal` (or `assert_series_equal` when the \
result is a Series): assert_frame_equal(fn(df), expected). This pins values, row \
order, AND dtype — construct `expected` with the intended dtypes and column/row order.
- Match the test to the NATURAL return type. If the idiom's natural answer is a \
scalar or bool, return that value and assert it directly (e.g. `assert fn(df) is True`, \
`assert fn(df) == 42`) — do NOT wrap a scalar in a 1x1 DataFrame just to use \
assert_frame_equal. If it is a Series, return the Series and use assert_series_equal. \
Reserve assert_frame_equal for answers that are genuinely DataFrames.
- If the slug is about numpy arrays (the numpy-foundations chapter), the \
entry_point takes and returns a numpy `ndarray` — return the ndarray, do NOT wrap \
it in a Series or DataFrame, and assert with `np.testing.assert_array_equal` \
(exact) or `np.testing.assert_allclose` (floats). Cover the element VALUES, not \
just dtype or type.
- Each edge test targets one property, e.g. that the input is not mutated \
(check the caller's frame is unchanged after the call) or an empty-input case.
- Every test is self-contained: it imports pandas (and assert_frame_equal) itself \
and constructs its own inputs. `fn` is the injected entry_point.
- NEVER use `equal(a, b)` on a DataFrame or Series — it cannot compare them and errors.

PROMPT RENDERING: when the task involves a DataFrame, describe the input and the \
expected result as monospace ASCII tables (assume a monospace font), using blank \
lines and alignment for structure — show the columns (df.columns) across the top, \
the row index (df.index) down the left, and note the corner (df.index.name / \
df.columns.name) when relevant. For a MultiIndex, stack the levels outward from the \
frame. Keep the task statement to one clear sentence near the table. Example layout:

              col_a  col_b  col_c   <- columns (df.columns)
            +------+------+------+
  idx_0     |  ... |  ... |  ... |
  idx_1     |  ... |  ... |  ... |
    ^
    +-- index (df.index)

Worked example — prompt renders the frame, tests use the hybrid contract:
  prompt: "Given df, return a new frame with a 'total' column = a + b.\\n\\n"
          "   a  b\\n 0  1 10\\n 1  2 20"
  canonical_answer: "import pandas as pd\\n\\ndef add_total(df):\\n    out = df.copy()\\n    out['total'] = df['a'] + df['b']\\n    return out"
  tests:
    - exact: build df and expected frames, assert_frame_equal(fn(df), expected)
    - edge:  after fn(df), assert 'total' not in df.columns (no mutation)
"""

PROFILES: dict[str, CorpusProfile] = {
    "python": CorpusProfile("python", _PYTHON_SECTION),
    "pandas": CorpusProfile("pandas", _PANDAS_SECTION),
}


def profile_for(corpus: str) -> CorpusProfile:
    return PROFILES.get(corpus, PROFILES["python"])
