# Fluency Driller

[![CI](https://github.com/jfdasher/fluency-driller/actions/workflows/ci.yml/badge.svg)](https://github.com/jfdasher/fluency-driller/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Spaced-repetition drills for programming idioms, run right in your editor or REPL.

Fluency Driller is for experienced programmers who already *know* an idiom and want
to keep recalling it quickly. You pull a small, atomic question into IPython or
Neovim, write the solution, run its tests, and submit. A cheap LLM judge then decides
whether your answer **demonstrates the target idiom**. Passing the tests isn't enough:
a `for` loop that builds a list passes the tests but fails a list-comprehension drill.
Each result feeds an SM-2 scheduler that uses recall latency, hints taken and
cheats to decide when the card comes back.

```text
In [1]: %drill next comprehension
Question #9 comprehensions/basic/even-squares-list-comp [comprehensions/basic] loaded into the next cell. (10 available: 0 due, 10 new)

In [2]: # Write a function `even_squares(nums)` that takes a list of integers and returns a new
   ...: # list containing the squares of only the even numbers, using a list comprehension.
   ...: def even_squares(nums):
   ...:     return [n * n for n in nums if n % 2 == 0]

In [3]: %drill test
5 passed, 0 failed.

In [4]: %drill submit
✅ pass #9 comprehensions/basic/even-squares-list-comp — All self-reported tests passed.
   next review: ~14min  ·  LEARNING, scheduled
      if GOOD ~14min · if EASY ~2d · if HARD ~0min
```

(Session above uses the offline `deterministic` judge. With the Anthropic judge,
the comment explains whether and why the idiom was demonstrated.)

## Features

- **Idiom-aware judging.** The answer text and self-reported test results go to
  Claude Haiku (configurable), which returns a structured verdict. The judge is a
  small swappable interface, and a `deterministic` judge works fully offline.
- **Spaced repetition.** SM-2 grading folds over an append-only event log. Recall
  latency is measured against a typing budget, and you can steer it by hand with
  `soon` and `bury`.
- **Hint ladder.** Each question has three tiers of hints, plus `cheat` to reveal the
  canonical answer (graded HARD).
- **Two clients.** An IPython `%drill` magic with keybindings, and a Neovim plugin
  (`lua/drill/`) driven by a Python sidecar.
- **Content corpora.** 156 Python questions across 11 chapters
  (comprehensions, iteration, stdlib, gotchas, …) and 70 pandas/NumPy questions across
  11 chapters (selection, groupby, reshaping, …), each one a plain directory on disk.
- **Content pipeline.** `drill-generate` drafts questions with an LLM in a
  verify-and-repair loop, and `drill-build-manifest` re-runs every question's tests
  against its canonical answer before anything can be imported.
- **Statistics.** Per-day, per-session, per-topic, trend and coverage views.

## Architecture

```text
 IPython %drill ──┐                    ┌── SQLite (questions, topics,
                  ├── HTTP ──▶ FastAPI │    append-only events)
 Neovim plugin ───┘  (signed   proctor ├── Judge: Anthropic | deterministic
  (Python sidecar)    cookie)          └── Scheduler: SM-2 over events
```

- The proctor is **stateless**. All persistent state lives in SQLite, and the
  session lives in a signed cookie.
- **The server never runs your code.** Tests run client-side, and the judge sees
  only the answer text and the reported results. This is a single-user,
  local-first tool by design: there is no auth and no sandbox. See the
  [PRD](docs/fluency-drill-prd.md) §4.

## Quick start

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
export DRILL_DB_PATH=drill.db

# Load the question corpora (idempotent; re-run after content changes)
uv run drill-import content/python/manifest.json
uv run drill-import content/pandas/manifest.json

# Start the proctor: real judging…
export ANTHROPIC_API_KEY=sk-ant-...
# …or fully offline:
# export DRILL_JUDGE=deterministic
scripts/drill-server up        # or: uv run uvicorn --factory drill.server.app:create_app
```

### IPython

```bash
uv run ipython
```

```python
%load_ext drill.client
%drill help
```

| Command | Alias | |
|---|---|---|
| `%drill next [KW]` | `%dn` | Fetch the next due question (optionally filtered by topic keyword) |
| `%drill test` | `%dt` | Run the question's tests against your function |
| `%drill submit` | `%ds` | Run tests; if they pass, submit for judging |
| `%drill hint` / `cheat` | `%dh` / `%dc` | Next hint / reveal the canonical answer |
| `%drill soon` / `bury` | `%dso` / `%dby` | Bring the card back soon / push it far out |
| `%drill corpus NAME` | | Restrict the session to one corpus (`python`, `pandas`, `all`) |
| `%drill stats [view]` | `%dstat` | `day`, `session`, `topics`, `trends`, `cards`, `coverage` |

On an empty cell, `Ctrl+]` is a smart advance (next, or submit), `Alt+N` fetches
the next question and `Alt+S` submits.

### Neovim

Add this repo to your runtime path (e.g. with lazy.nvim, `dir = "~/path/to/fluency-driller"`)
and call:

```lua
require("drill").setup({
  url = "http://127.0.0.1:8000",
  cwd = vim.fn.expand("~/path/to/fluency-driller"),  -- where `uv run python` finds the drill package
})
```

Then use `:Drill next`, `:Drill submit`, and so on, or the `<leader>d…` keymaps
(`dn` next, `dt` test + submit, `dh` hint, `dc` cheat, `dS` stats).

## Configuration

| Env var | Default | Purpose |
|---|---|---|
| `DRILL_DB_PATH` | `drill.db` | SQLite file |
| `ANTHROPIC_API_KEY` | | Required for the Anthropic judge |
| `DRILL_JUDGE` | `anthropic` | `anthropic` \| `deterministic` |
| `DRILL_MODEL` | `claude-haiku-4-5` | Judge model |
| `DRILL_JUDGE_TIMEOUT` | `30.0` | Judge API timeout (seconds) |
| `DRILL_SESSION_SECRET` | random per start | Signs the session cookie |
| `DRILL_URL` | `http://127.0.0.1:8000` | Proctor URL (client) |
| `DRILL_USER` | `anon` | User name recorded on events (client) |
| `DRILL_CORPUS` | all corpora | Default corpus selection (client) |

## Writing questions

Each question is a directory:

```text
content/<corpus>/<topic>/<name>/      e.g. content/python/comprehensions/basic/even-squares-list-comp/
  question.md           YAML frontmatter (topic, entry point, status) + prompt + hints
  stub.py               skeleton the user starts from
  canonical_answer.py   reference solution
  tests/<name>.py       plain assert-based tests
```

Write one by hand, or draft a batch for a topic with
`uv run drill-generate --corpus python comprehensions/basic -n 3` (needs `ANTHROPIC_API_KEY`).
Generated questions start out as `status: draft`. Review them, set them to `approved`, then rebuild and import:

```bash
uv run drill-build-manifest content/python    # re-verifies every question
uv run drill-import content/python/manifest.json
```

The build refuses any question whose canonical answer fails its own tests.

## Development

```bash
uv run pytest         # full suite, offline: no API key, no network
uv run ruff check .
```

The full product spec is [`docs/fluency-drill-prd.md`](docs/fluency-drill-prd.md).

## License

[MIT](LICENSE) © James Dasher
