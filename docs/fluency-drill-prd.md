# PRD: Fluency Drill System (MVP)

**Status:** Implemented (MVP spec; later features extend it)
**Owner:** James Dasher
**Date:** 2026-06-10

---

## 1. Problem

Working programmers lose recall fluency in language idioms they rarely exercise (e.g., multi-key stable sorts with mixed directions). Interview and real-time coding contexts punish slow recall even when understanding is intact. Existing tools (Anki, LeetCode) either lack executable grading, don't live in the editor, or test recognition rather than production.

## 2. Product summary

A three-part system:

1. **Question store** — SQLite database of atomic, idiom-level drill questions across languages, with canonical answers, test cases, and progressive hint ladders.
2. **Proctor service** — A small, stateless FastAPI HTTP service that delivers questions and judges submissions. Judgment of *intent* (did the answer demonstrate the target idiom, not merely pass tests) is delegated to a single cheap LLM call (Haiku-class).
3. **IPython client** — A `%drill` magic that injects questions into the REPL as editable cells and submits answers for judgment. Execution happens client-side; the server never runs user code.

A separate, offline **batch writer** (expensive model, run occasionally) generates question content. It is out of scope for the MVP build except as a JSON import format; the MVP ships with a hand-seeded question set.

## 3. Goals (MVP)

- Complete drill loop in IPython: fetch → edit → run → submit → verdict/hint, in under 5 seconds round-trip excluding user think time.
- Deterministic, append-only event log sufficient to retroactively train/configure any future scheduler (FSRS, SM-2) without data loss.
- Polyglot-ready data model from day one (questions carry a `language`/`runtime` field), even though only Python questions and the Python client ship in MVP.
- Zero infrastructure: one SQLite file, one Python service, one client module. `cp` is the backup strategy.

## 4. Non-goals (MVP)

- No server-side sandbox. Client self-reports test output; trust model is honor-system (single-user self-study tool). Do not build anything credential-like on this data.
- No Neovim or VS Code clients. (Protocol must not preclude them; see §6.)
- No multi-user auth. A `user` string parameter is carried through for future use; no auth, no accounts.
- No batch-writer agent. Define the import JSON format; seed manually.
- No anti-cheat, no leaderboards, no web UI.

## 5. Architecture

```
┌─────────────┐   HTTP/JSON    ┌──────────────┐   1 call/submit   ┌────────┐
│ IPython     │ ─────────────► │ Proctor      │ ────────────────► │ LLM    │
│ %drill magic│ ◄───────────── │ (FastAPI)    │ ◄──────────────── │ judge  │
└─────────────┘                └──────┬───────┘                   └────────┘
  executes code                       │
  locally                       ┌─────▼──────┐
                                │ SQLite     │
                                │ drill.db   │
                                └────────────┘
```

- Transport: plain HTTP + JSON. No RPC framing, no gRPC, no websockets. `curl` must be a usable test harness.
- Proctor is stateless; all state lives in SQLite.
- Client-side execution: the IPython client runs the user's code and includes captured test output in the submission. The judge sees answer text + self-reported test results.

## 6. API

### `GET /next?user={user}&language={language?}`

Returns the next question per the scheduler (§7).

```json
{
  "question_id": 42,
  "topic": "sorting/multi-key-stable",
  "language": "python",
  "modality": "code",
  "prompt": "Sort dict d (str -> str of int) ascending by int value, descending lexicographic by key as tiebreak. Return list of (k, v) tuples.",
  "stub": "def solve(d):\n    ...",
  "entry_point": "solve",
  "test_cases": [
    {"input": {"d": {"a": "2", "b": "1", "c": "2"}},
     "expected": [["b", "1"], ["c", "2"], ["a", "2"]]}
  ],
  "due_count": 3,
  "new_count": 2
}
```

`due_count` and `new_count` are a snapshot of what is available to drill right
now — cards due for review and never-seen cards respectively, *including* the
card being returned. Their sum reaches zero exactly when `/next` would `404`.
The client surfaces them in the "loaded" notification.

`404` with `{"detail": "no questions remaining"}` when the queue is exhausted.

`entry_point` names the function the client must define, call for test cases
(`entry_point(**test_case.input)`), and read back via `inspect.getsource` on
submit. Defaults to `solve`.

### `POST /submit`

```json
{
  "user": "jim",
  "question_id": 42,
  "answer_text": "def solve(d):\n    items = sorted(d.items(), key=lambda kv: kv[0], reverse=True)\n    return sorted(items, key=lambda kv: int(kv[1]))",
  "test_output": {"passed": 3, "failed": 0, "detail": []},
  "latency_ms": 48000,
  "hints_already_shown": 0
}
```

Response:

```json
{
  "verdict": "pass",          // pass | pass_hinted | fail
  "hint": null,                // populated on fail, if hints remain
  "hint_index": null,
  "judge_comment": "Two-pass stable sort correctly demonstrates the idiom."
}
```

Semantics:

- **Judge prompt contract.** The LLM judge receives: target topic/idiom, prompt, canonical answer, the submitted answer, and self-reported test output. It returns structured JSON: `{verdict_proposal: pass|fail, demonstrates_idiom: bool, hint_index: int|null, comment: str}`. Passing tests with the wrong idiom (e.g., hand-rolled comparison loop instead of `sorted` with `key`) is a **fail** with a hint pointing at the idiom.
- **Verdict authority.** The judge is authoritative. The server uses
  `verdict_proposal` verbatim and does **not** independently gate on `test_output`
  (the trust model is honor-system, single-user). `demonstrates_idiom` is an
  advisory signal: it is logged but does not override `verdict_proposal`. The
  server maps `verdict_proposal` to the stored verdict by `hints_already_shown`:
  - `verdict_proposal == pass` and `hints_already_shown == 0` → `pass`
  - `verdict_proposal == pass` and `hints_already_shown > 0`  → `pass_hinted`
  - `verdict_proposal == fail` → `fail`
- **Hint ladder.** Hints are an ordered list per question. On fail, the server returns the hint at `hints_already_shown` (or the judge's `hint_index` if it identifies a more relevant one — judge's choice wins). When hints are exhausted, return `hint: null` and the canonical answer in `judge_comment`.
- **`pass_hinted`.** A pass on a submission where `hints_already_shown > 0`. The dumb scheduler treats `pass_hinted` as not-yet-answered (it will be served again).
- Every call to `/submit` appends exactly one row to `events`. No updates to `events`, ever.

### Error handling

- LLM judge unavailable/timeout (5s): return `503` with retry guidance; log nothing to `events`.
- Malformed judge output: one retry with a corrective message; then `503`.

## 7. Scheduler (SM-2 spaced repetition)

Uses the SM-2 algorithm with Anki-style learning steps. The scheduler is a
pure fold over the append-only `events` log — no mutable per-card state.

**Grade mapping** (`drill/server/srs.py`):

| Event verdict | Grade |
|---|---|
| `fail` | AGAIN |
| `pass_hinted` | HARD (needed help; not fluent) |
| `pass`, hesitation ≤ 2 s | EASY |
| `pass`, hesitation > 2 s | GOOD |

Hesitation = `max(0, latency_ms − 120 × len(answer_text))` (typing time removed).

**SM-2 transitions:**

- **Learning / Relearning steps:** 1 min → 10 min. AGAIN → step 0; HARD → repeat current step; GOOD → next step (or graduate); EASY → graduate immediately.
- **Graduation → Review:** interval = 1 day, ease = 2.5.
- **Review:** GOOD → `interval × ease`; EASY → `interval × ease × 1.3`; HARD → `interval × 1.2`, ease −0.2; AGAIN → lapse, ease −0.2, enter Relearning.
- Ease is floored at 1.3.

**Selection** (`next_question`): among cards with `due_at ≤ now`, serve the most overdue (smallest `due_at`), tiebreak ascending `question_id`. If none are due, serve the lowest-id NEW card. If nothing is due and no new cards remain → `None` ("nothing due right now").

Signature: `next_question(conn, user, language=None, topic=None, topic_keyword=None, *, now=None, cfg=None) -> Question | None`.

## 8. Data model

SQLite, `PRAGMA journal_mode=WAL`.

```sql
CREATE TABLE questions (
  id               INTEGER PRIMARY KEY,
  external_id      TEXT UNIQUE,              -- stable author-controlled id; import upsert key
  topic            TEXT NOT NULL,            -- e.g. 'sorting/multi-key-stable'
  language         TEXT NOT NULL,            -- e.g. 'python'
  modality         TEXT NOT NULL CHECK (modality IN ('code','fill_in')),
  prompt           TEXT NOT NULL,
  stub             TEXT,
  entry_point      TEXT NOT NULL DEFAULT 'solve',  -- function the client defines/calls
  canonical_answer TEXT NOT NULL,
  hints_json       TEXT NOT NULL DEFAULT '[]',   -- ordered list of strings
  test_cases_json  TEXT NOT NULL DEFAULT '[]'     -- each: {input: {kwargs}, expected: ...}
);

CREATE TABLE events (
  id                 INTEGER PRIMARY KEY,
  user               TEXT NOT NULL,
  question_id        INTEGER NOT NULL REFERENCES questions(id),
  ts                 TEXT NOT NULL DEFAULT (datetime('now')),  -- ISO 8601 UTC
  verdict            TEXT NOT NULL CHECK (verdict IN ('pass','pass_hinted','fail')),
  hint_index         INTEGER,            -- hint returned with this verdict, if any
  hints_shown        INTEGER NOT NULL DEFAULT 0,  -- as reported at submission time
  latency_ms         INTEGER,
  answer_text        TEXT NOT NULL,
  judge_comment      TEXT,
  demonstrates_idiom INTEGER,            -- advisory judge signal (0/1), logged not enforced
  judge_json         TEXT                 -- raw judge payload, for retroactive analysis
);
-- events is append-only. No UPDATE or DELETE paths in application code.
```

`topics` table deferred; `topic` is a slash-delimited string for now (sortable, splittable later).

### Question import format

A JSON array of question objects matching the `questions` columns (hints and test cases as native JSON arrays; each test case is `{"input": {kwargs}, "expected": ...}`, invoked as `entry_point(**input)`). One idempotent import script: `python -m drill.server.importer questions.json`, which **upserts on `external_id`** — every seed question carries a stable `external_id` so prompts stay editable without creating duplicates.

### Question granularity standard (for content authors)

One question = one retrievable idiom, answerable in 1–5 lines, 30–90 seconds. "Stable multi-key sort with mixed directions" is one question; "sorting" is a topic.

## 9. IPython client

A module loadable via `%load_ext drill.client` (the client lives in the single
`drill` package; IPython accepts dotted module paths), configured by env vars
(`DRILL_URL`, `DRILL_USER`).

- `%drill next [language]` — GET `/next`, then `get_ipython().set_next_input()` with the prompt rendered as comments, followed by the stub. Stores `question_id`, fetch timestamp, `entry_point`, and `test_cases` in client state. On `404` (queue exhausted), prints a friendly message and clears state.
- `%drill test` — resolves the function named by `entry_point` in the user namespace, runs the stored test cases as `entry_point(**input)`, prints results, caches `test_output`.
- `%drill submit` — resolves the `entry_point` function and captures its source via `inspect.getsource` (robust to which cell ran it; IPython registers cell sources in `linecache`). POSTs that `answer_text`, cached `test_output`, computed `latency_ms` (submit time − fetch time), and the running hint count. Prints verdict; on fail with hint, prints the hint and increments the local hint counter.
- `%drill skip` — clears client state without logging an event.

Client must degrade gracefully: if `%drill test` was never run, submit with `test_output: null` (the judge is told tests were not run).

## 10. Tech stack

- Python 3.11+ (packaged with `uv`), FastAPI + uvicorn, stdlib `sqlite3`, `httpx` in the client.
- A single installable `drill` package (server + client + data), so the client loads as `%load_ext drill.client`.
- LLM judge behind a `Judge` interface so it is swappable and testable:
  - `AnthropicJudge` — Anthropic API, default model `claude-haiku-4-5` (configurable via env var), small `max_tokens`, schema-valid structured output (`messages.parse`). The call pins a hard 5 s timeout and disables SDK auto-retries so the §6 503 budget holds.
  - `DeterministicJudge` — a toy that decides from the self-reported `test_output` (no network). Used for the offline test suite and `curl`-only demos; selected via `DRILL_JUDGE`. The full suite runs with no API key.
- Single repo, layout:

```
drill/
  server/      # FastAPI app, scheduler, judge, db
  client/      # IPython extension
  data/        # seed questions JSON
  tests/
```

## 11. Seed content

≥ 15 hand-written Python questions across ≥ 4 topics (suggested: sorting/key-functions, comprehensions, string-methods, dict-idioms), each with 2–3 hints and ≥ 2 test cases. The first question must be the multi-key stable sort that motivated this project.

## 12. Acceptance criteria

1. `uvicorn` up, `%load_ext drill.client`, `%drill next` injects a question into the REPL.
2. Submitting the canonical answer yields `pass` and one new `events` row.
3. Submitting a test-passing but idiom-missing answer (hand-rolled loop for the sort question) yields `fail` with a hint.
4. Submitting a correct answer after a hint yields `pass_hinted`; the question re-enters the learning queue (HARD grade — repeats current learning step).
5. A failed question (AGAIN) enters the 1-minute learning step; a just-failed card is not re-served until the step expires.
6. `curl` alone can drive the full loop (documented in README).
7. `events` contains every submission with latency and answer text; no code path mutates existing rows.
8. Server runs with only `DRILL_DB_PATH` and `ANTHROPIC_API_KEY` set.

## 13. Future work (explicitly deferred)

- ~~FSRS/SM-2 scheduler as a pure function over the `events` stream.~~ ✓ Delivered (SM-2 with Anki learning steps; see §7).
- Batch question-writer agent (Sonnet-class) emitting the import format, with executable verification of generated test cases.
- Neovim client (plenary.curl); possible LSP-shim architecture so verdicts render as diagnostics in any LSP editor.
- VS Code extension.
- Per-language AST fast-path checks ahead of the LLM judge.
- `topics` table and taxonomy management.
- Latency-aware fluency scoring.
