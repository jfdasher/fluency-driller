"""Pure SM-2 spaced-repetition engine.

No database, no wall clock. All inputs are passed in; all outputs are plain
data — safe to unit-test deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class Grade(Enum):
    AGAIN = "AGAIN"
    HARD = "HARD"
    GOOD = "GOOD"
    EASY = "EASY"


_GRADE_ORDER = {Grade.AGAIN: 0, Grade.HARD: 1, Grade.GOOD: 2, Grade.EASY: 3}


def _cap(grade: Grade, ceiling: Grade) -> Grade:
    """Return grade unless it ranks above ceiling, in which case return ceiling."""
    return grade if _GRADE_ORDER[grade] <= _GRADE_ORDER[ceiling] else ceiling


@dataclass
class SrsConfig:
    learning_steps_min: tuple[int, ...] = (1, 10)
    graduating_interval_days: float = 1.0
    easy_interval_days: float = 2.0  # was 4.0
    starting_ease: float = 1.8  # was 2.5
    min_ease: float = 1.3
    easy_bonus: float = 1.15  # was 1.3
    hard_multiplier: float = 1.2
    lapse_ease_penalty: float = 0.2
    ms_per_char: int = 500  # was 250 (2026-06-30: matched to measured typing rate)
    hesitation_fast_ms: int = 20000
    bury_interval_days: float = 21.0
    winsor_ms: float = 300000.0  # clean passes slower than this can't earn EASY


@dataclass
class CardState:
    phase: str  # "NEW" | "LEARNING" | "REVIEW" | "RELEARNING"
    due_at: datetime
    interval: float  # days (0 for learning/relearning phases)
    ease: float
    step_idx: int = 0  # index into cfg.learning_steps_min (LEARNING/RELEARNING)


def derive_grade(
    verdict: str,
    hints_shown: int,
    latency_ms: int | None,
    typed_chars: int,
    cfg: SrsConfig,
) -> Grade:
    if verdict == "fail":
        return Grade.AGAIN
    if verdict == "pass_hinted":
        return Grade.HARD
    # verdict == "pass"
    if latency_ms is None:
        return Grade.GOOD
    if latency_ms > cfg.winsor_ms:
        # An over-cap timing is untrustworthy (walk-away, long iteration); it
        # forfeits the fast-recall reward. Never *promotes* a grade.
        return Grade.GOOD
    hesitation = max(0, latency_ms - cfg.ms_per_char * typed_chars)
    return Grade.EASY if hesitation <= cfg.hesitation_fast_ms else Grade.GOOD


def step(state: CardState, grade: Grade, ts: datetime, cfg: SrsConfig) -> CardState:
    """Apply one already-resolved grade to a card state, returning the next state.

    Pure: no clock, no poisoning/cheat logic (the caller resolves the final
    grade before calling). ``ts`` is the submission time the schedule is
    measured from.
    """
    phase, step_idx = state.phase, state.step_idx
    ease, interval, due_at = state.ease, state.interval, state.due_at

    if phase == "NEW":
        phase = "LEARNING"

    if phase in ("LEARNING", "RELEARNING"):
        was_relearning = phase == "RELEARNING"
        if grade == Grade.AGAIN:
            step_idx = 0
            due_at = ts + timedelta(minutes=cfg.learning_steps_min[0])
        elif grade == Grade.HARD:
            due_at = ts + timedelta(minutes=cfg.learning_steps_min[step_idx])
        elif grade == Grade.GOOD:
            if step_idx < len(cfg.learning_steps_min) - 1:
                step_idx += 1
                due_at = ts + timedelta(minutes=cfg.learning_steps_min[step_idx])
            else:
                phase = "REVIEW"
                interval = cfg.graduating_interval_days
                if not was_relearning:
                    ease = cfg.starting_ease
                due_at = ts + timedelta(days=interval)
                step_idx = 0
        elif grade == Grade.EASY:
            phase = "REVIEW"
            interval = cfg.easy_interval_days
            if not was_relearning:
                ease = cfg.starting_ease
            due_at = ts + timedelta(days=interval)
            step_idx = 0

    elif phase == "REVIEW":
        if grade == Grade.AGAIN:
            ease = max(cfg.min_ease, ease - cfg.lapse_ease_penalty)
            phase = "RELEARNING"
            step_idx = 0
            due_at = ts + timedelta(minutes=cfg.learning_steps_min[0])
        elif grade == Grade.HARD:
            ease = max(cfg.min_ease, ease - cfg.lapse_ease_penalty)
            interval *= cfg.hard_multiplier
            due_at = ts + timedelta(days=interval)
        elif grade == Grade.GOOD:
            interval *= ease
            due_at = ts + timedelta(days=interval)
        elif grade == Grade.EASY:
            interval *= ease * cfg.easy_bonus
            due_at = ts + timedelta(days=interval)

    return CardState(phase=phase, due_at=due_at, interval=interval, ease=ease, step_idx=step_idx)


def replay(
    events: list[dict[str, Any]],
    cfg: SrsConfig,
    now: datetime,
) -> CardState:
    """Folds submission/cheat/soon/bury events into a CardState.

    Events are folded in timestamp order; events sharing a timestamp (e.g. a
    cheat and its following submission in the same second) must be supplied in
    insertion order — ``scheduler_events_for_user`` guarantees this via
    ORDER BY ts, id.
    """
    if not events:
        return CardState(phase="NEW", due_at=now, interval=0.0, ease=cfg.starting_ease)

    phase = "NEW"
    step_idx = 0
    ease = cfg.starting_ease
    interval = 0.0
    due_at = now
    poisoned = False  # a cheat caps the next submission's grade

    for event in sorted(events, key=lambda e: e["ts"]):
        ts: datetime = event["ts"]
        kind = event.get("kind", "submission")

        if kind == "cheat":
            poisoned = (
                True  # consumed by the next submission; survives intervening soon/bury events
            )
            continue
        if kind == "soon":
            phase = "RELEARNING"
            step_idx = 0
            interval = 0.0
            due_at = ts + timedelta(minutes=cfg.learning_steps_min[0])
            continue
        if kind == "bury":
            phase = "REVIEW"
            interval = max(interval, cfg.bury_interval_days)
            due_at = ts + timedelta(days=interval)
            continue
        if kind != "submission":
            continue  # unknown kinds are inert

        typed_chars = max(
            0,
            len(event.get("answer_text", "")) - (event.get("prefill_chars") or 0),
        )
        grade = derive_grade(
            event["verdict"],
            event.get("hints_shown", 0),
            event.get("latency_ms"),
            typed_chars,
            cfg,
        )
        if poisoned:
            grade = _cap(grade, Grade.HARD)
            poisoned = False

        state = step(
            CardState(phase=phase, due_at=due_at, interval=interval, ease=ease, step_idx=step_idx),
            grade,
            ts,
            cfg,
        )
        phase, due_at, interval, ease, step_idx = (
            state.phase,
            state.due_at,
            state.interval,
            state.ease,
            state.step_idx,
        )

    return CardState(phase=phase, due_at=due_at, interval=interval, ease=ease, step_idx=step_idx)
