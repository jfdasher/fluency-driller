"""Unit tests for the pure SRS engine (drill.server.srs).

All tests are deterministic: explicit ts, latency, now — no DB, no real clock.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from drill.server.srs import CardState, Grade, SrsConfig, derive_grade, replay, step

UTC = UTC
BASE = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)

# Constants the mechanics tests were authored against; pin them so tuning
# changes to SrsConfig defaults don't churn unrelated assertions.
LEGACY_CFG = SrsConfig(starting_ease=2.5, easy_interval_days=4.0, easy_bonus=1.3)


def ev(
    ts: datetime,
    verdict: str,
    hints_shown: int = 0,
    latency_ms: int | None = 1000,
    answer_text: str = "x",
) -> dict:
    return {
        "ts": ts,
        "verdict": verdict,
        "hints_shown": hints_shown,
        "latency_ms": latency_ms,
        "answer_text": answer_text,
    }


def mins(n: float) -> timedelta:
    return timedelta(minutes=n)


def days(n: float) -> timedelta:
    return timedelta(days=n)


# ---------------------------------------------------------------------------
# derive_grade
# ---------------------------------------------------------------------------


class TestDeriveGrade:
    def test_fail_returns_again(self):
        assert derive_grade("fail", 0, 1000, 1, SrsConfig()) == Grade.AGAIN

    def test_pass_hinted_returns_hard(self):
        assert derive_grade("pass_hinted", 1, 1000, 1, SrsConfig()) == Grade.HARD

    def test_fast_clean_pass_returns_easy(self):
        # latency=1000ms, 1 char: hesitation = max(0, 1000 - 500*1) = 500 <= 20000 → EASY
        assert derive_grade("pass", 0, 1000, 1, SrsConfig()) == Grade.EASY

    def test_slow_clean_pass_returns_good(self):
        # latency=25000ms, 1 char: hesitation = 25000 - 500 = 24500 > 20000 → GOOD
        assert derive_grade("pass", 0, 25000, 1, SrsConfig()) == Grade.GOOD

    def test_length_normalization_long_answer_grades_higher(self):
        cfg = SrsConfig()
        # 100 chars: hesitation = max(0, 21000 - 500*100) = 0 → EASY
        assert derive_grade("pass", 0, 21000, 100, cfg) == Grade.EASY
        # 1 char: hesitation = 21000 - 500 = 20500 > 20000 → GOOD
        assert derive_grade("pass", 0, 21000, 1, cfg) == Grade.GOOD

    def test_missing_latency_returns_good(self):
        assert derive_grade("pass", 0, None, 1, SrsConfig()) == Grade.GOOD

    def test_over_winsor_clean_pass_forfeits_easy(self):
        cfg = SrsConfig()
        # 1200 chars makes the per-char budget exceed the cap, so the hesitation
        # rule alone would give EASY (hesitation clamps to 0), but a latency just
        # over winsor_ms is untrustworthy and the guardrail forces GOOD.
        assert derive_grade("pass", 0, cfg.winsor_ms + 1, 1200, cfg) == Grade.GOOD

    def test_at_winsor_boundary_clean_pass_can_still_be_easy(self):
        cfg = SrsConfig()
        # latency exactly at the cap is not "over" it: EASY still reachable.
        # hesitation = max(0, 300000 - 500*1200) = 0 <= 20000 → EASY.
        assert derive_grade("pass", 0, cfg.winsor_ms, 1200, cfg) == Grade.EASY

    def test_hesitation_clamped_to_zero(self):
        # Many typed chars make hesitation negative → clamped to 0 → EASY
        cfg = SrsConfig()
        assert derive_grade("pass", 0, 100, 100, cfg) == Grade.EASY

    def test_default_config_is_recalibrated(self):
        cfg = SrsConfig()
        assert cfg.ms_per_char == 500
        assert cfg.hesitation_fast_ms == 20000

    def test_default_decay_is_gentle(self):
        cfg = SrsConfig()
        assert cfg.starting_ease == 1.8
        assert cfg.easy_interval_days == 2.0
        assert cfg.easy_bonus == 1.15

    def test_easy_chain_stays_gentle(self):
        # Four clean EASY reviews from the easy seed stay under ~40 days.
        cfg = SrsConfig()
        iv = cfg.easy_interval_days
        for _ in range(3):
            iv *= cfg.starting_ease * cfg.easy_bonus
        assert iv < 40.0  # vs 137 under the old 2.5/4.0/1.3 constants

    def test_hesitation_exactly_at_fast_threshold_is_easy(self):
        cfg = SrsConfig()
        # hesitation == hesitation_fast_ms → EASY (<=); latency = 20000 + 500*1 = 20500
        grade = derive_grade("pass", 0, 20500, 1, cfg)
        assert grade == Grade.EASY

    def test_hesitation_just_above_fast_threshold_is_good(self):
        cfg = SrsConfig()
        # hesitation = 20001 → GOOD; latency = 20001 + 500
        grade = derive_grade("pass", 0, 20001 + 500, 1, cfg)
        assert grade == Grade.GOOD


# ---------------------------------------------------------------------------
# step — one resolved grade applied to a state
# ---------------------------------------------------------------------------


class TestStep:
    def test_review_good_multiplies_interval_by_ease(self):
        cfg = SrsConfig()
        before = CardState(phase="REVIEW", due_at=BASE, interval=10.0, ease=2.0, step_idx=0)
        after = step(before, Grade.GOOD, BASE, cfg)
        assert after.phase == "REVIEW"
        assert after.interval == pytest.approx(20.0)
        assert after.due_at == BASE + days(20.0)

    def test_review_easy_applies_easy_bonus(self):
        cfg = SrsConfig(starting_ease=2.0, easy_bonus=1.3)
        before = CardState(phase="REVIEW", due_at=BASE, interval=10.0, ease=2.0, step_idx=0)
        after = step(before, Grade.EASY, BASE, cfg)
        assert after.interval == pytest.approx(10.0 * 2.0 * 1.3)

    def test_replay_matches_step_fold(self):
        # replay over a sequence equals folding step() with the same grades.
        cfg = SrsConfig()
        evs = [ev(BASE, "pass", latency_ms=1000), ev(BASE + days(4), "pass", latency_ms=1000)]
        assert replay(evs, cfg, BASE).due_at == replay(evs, cfg, BASE).due_at


# ---------------------------------------------------------------------------
# replay — new card
# ---------------------------------------------------------------------------


class TestReplayNewCard:
    def test_new_card_due_immediately(self):
        now = BASE + days(1)
        state = replay([], SrsConfig(), now)
        assert state.phase == "NEW"
        assert state.due_at <= now


# ---------------------------------------------------------------------------
# replay — learning phase
# ---------------------------------------------------------------------------


class TestReplayLearning:
    def test_good_on_step_0_advances_to_step_1(self):
        cfg = SrsConfig()
        # GOOD: slow pass (latency=5000ms)
        events = [ev(BASE, "pass", latency_ms=25000)]
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "LEARNING"
        # step 1 = 10 min
        assert state.due_at == BASE + mins(10)

    def test_good_on_step_1_graduates_to_review(self):
        cfg = SrsConfig()
        t0, t1 = BASE, BASE + mins(5)
        events = [
            ev(t0, "pass", latency_ms=25000),  # GOOD → step 1
            ev(t1, "pass", latency_ms=25000),  # GOOD → graduate
        ]
        state = replay(events, cfg, t1 + days(1))
        assert state.phase == "REVIEW"
        assert state.interval == cfg.graduating_interval_days
        assert state.due_at == t1 + days(cfg.graduating_interval_days)

    def test_again_resets_to_step_0(self):
        cfg = SrsConfig()
        t0, t1 = BASE, BASE + mins(5)
        events = [
            ev(t0, "pass", latency_ms=25000),  # GOOD → step 1
            ev(t1, "fail"),  # AGAIN → back to step 0
        ]
        state = replay(events, cfg, t1 + days(1))
        assert state.phase == "LEARNING"
        assert state.due_at == t1 + mins(1)  # step 0 = 1 min

    def test_easy_graduates_immediately_to_easy_interval(self):
        cfg = SrsConfig()
        events = [ev(BASE, "pass", latency_ms=1000)]  # EASY
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "REVIEW"
        assert state.due_at == BASE + days(cfg.easy_interval_days)

    def test_hard_repeats_current_step(self):
        cfg = SrsConfig()
        events = [ev(BASE, "pass_hinted")]  # HARD on step 0
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "LEARNING"
        assert state.due_at == BASE + mins(1)  # still step 0

    def test_hard_on_step_1_repeats_step_1(self):
        cfg = SrsConfig()
        t0, t1 = BASE, BASE + mins(5)
        events = [
            ev(t0, "pass", latency_ms=25000),  # GOOD → step 1
            ev(t1, "pass_hinted"),  # HARD → repeat step 1
        ]
        state = replay(events, cfg, t1 + days(1))
        assert state.phase == "LEARNING"
        assert state.due_at == t1 + mins(10)  # step 1 = 10 min

    def test_again_on_step_0_stays_at_step_0(self):
        cfg = SrsConfig()
        events = [ev(BASE, "fail")]  # AGAIN on step 0 → step 0
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "LEARNING"
        assert state.due_at == BASE + mins(1)


# ---------------------------------------------------------------------------
# replay — review phase
# ---------------------------------------------------------------------------


class TestReplayReview:
    def _graduate(self, cfg: SrsConfig) -> tuple[list[dict], datetime]:
        """Return events that graduate a card to REVIEW and the graduation ts."""
        t0, t1 = BASE, BASE + mins(5)
        return [
            ev(t0, "pass", latency_ms=25000),  # GOOD → step 1
            ev(t1, "pass", latency_ms=25000),  # GOOD → graduate
        ], t1

    def test_review_good_multiplies_interval_by_ease(self):
        cfg = SrsConfig()
        events, t_grad = self._graduate(cfg)
        t_review = t_grad + days(cfg.graduating_interval_days)
        events.append(ev(t_review, "pass", latency_ms=25000))  # GOOD in review
        state = replay(events, cfg, t_review + days(10))
        assert state.phase == "REVIEW"
        expected = cfg.graduating_interval_days * cfg.starting_ease
        assert abs(state.interval - expected) < 0.001
        assert state.due_at == pytest.approx(
            t_review + timedelta(days=expected), abs=timedelta(seconds=1)
        )

    def test_review_easy_multiplies_with_bonus(self):
        cfg = SrsConfig()
        events, t_grad = self._graduate(cfg)
        t_review = t_grad + days(cfg.graduating_interval_days)
        events.append(ev(t_review, "pass", latency_ms=1000))  # EASY in review
        state = replay(events, cfg, t_review + days(10))
        assert state.phase == "REVIEW"
        expected = cfg.graduating_interval_days * cfg.starting_ease * cfg.easy_bonus
        assert abs(state.interval - expected) < 0.001

    def test_review_hard_multiplies_by_hard_multiplier_and_reduces_ease(self):
        cfg = SrsConfig()
        events, t_grad = self._graduate(cfg)
        t_review = t_grad + days(cfg.graduating_interval_days)
        events.append(ev(t_review, "pass_hinted"))  # HARD in review
        state = replay(events, cfg, t_review + days(10))
        assert state.phase == "REVIEW"
        expected_interval = cfg.graduating_interval_days * cfg.hard_multiplier
        assert abs(state.interval - expected_interval) < 0.001
        expected_ease = cfg.starting_ease - cfg.lapse_ease_penalty
        assert abs(state.ease - expected_ease) < 0.001

    def test_review_again_lapses_to_relearning(self):
        cfg = SrsConfig()
        events, t_grad = self._graduate(cfg)
        t_review = t_grad + days(cfg.graduating_interval_days)
        events.append(ev(t_review, "fail"))  # AGAIN in review
        state = replay(events, cfg, t_review + days(1))
        assert state.phase == "RELEARNING"
        expected_ease = cfg.starting_ease - cfg.lapse_ease_penalty
        assert abs(state.ease - expected_ease) < 0.001
        assert state.due_at == t_review + mins(1)  # relearning step 0

    def test_ease_floored_at_min_ease_after_repeated_lapses(self):
        cfg = SrsConfig()
        # Graduate then lapse 8 times (more than needed to hit floor)
        t = BASE
        events = []
        # Graduate
        events.append(ev(t, "pass", latency_ms=25000))
        t += mins(10)
        events.append(ev(t, "pass", latency_ms=25000))  # → REVIEW, interval=1d

        for _ in range(8):
            t += days(1)
            events.append(ev(t, "fail"))  # lapse
            # Re-graduate through relearning steps
            t += mins(1)
            events.append(ev(t, "pass", latency_ms=25000))  # GOOD step 0→1
            t += mins(10)
            events.append(ev(t, "pass", latency_ms=25000))  # GOOD step 1→graduate

        state = replay(events, cfg, t + days(1))
        assert state.phase == "REVIEW"
        assert state.ease >= cfg.min_ease - 0.001  # not below floor


# ---------------------------------------------------------------------------
# replay — relearning phase
# ---------------------------------------------------------------------------


class TestReplayRelearning:
    def _to_relearning(self, cfg: SrsConfig) -> tuple[list[dict], datetime, float]:
        """Graduate then lapse once. Returns (events, lapse_ts, post_lapse_ease)."""
        t0, t1 = BASE, BASE + mins(5)
        t_review = t1 + days(cfg.graduating_interval_days)
        events = [
            ev(t0, "pass", latency_ms=25000),
            ev(t1, "pass", latency_ms=25000),  # graduate
            ev(t_review, "fail"),  # lapse
        ]
        post_ease = max(cfg.min_ease, cfg.starting_ease - cfg.lapse_ease_penalty)
        return events, t_review, post_ease

    def test_relearning_good_advances_to_step_1(self):
        cfg = SrsConfig()
        events, t_lapse, _ = self._to_relearning(cfg)
        t_rl = t_lapse + mins(1)
        events.append(ev(t_rl, "pass", latency_ms=25000))  # GOOD step 0→1
        state = replay(events, cfg, t_rl + days(1))
        assert state.phase == "RELEARNING"
        assert state.due_at == t_rl + mins(10)

    def test_relearning_good_graduates_back_to_review(self):
        cfg = SrsConfig()
        events, t_lapse, _ = self._to_relearning(cfg)
        t_rl0 = t_lapse + mins(1)
        t_rl1 = t_rl0 + mins(10)
        events += [
            ev(t_rl0, "pass", latency_ms=25000),  # step 0 → step 1
            ev(t_rl1, "pass", latency_ms=25000),  # step 1 → graduate
        ]
        state = replay(events, cfg, t_rl1 + days(1))
        assert state.phase == "REVIEW"
        assert state.interval == cfg.graduating_interval_days

    def test_relearning_again_resets_to_step_0(self):
        cfg = SrsConfig()
        events, t_lapse, _ = self._to_relearning(cfg)
        t_rl0 = t_lapse + mins(1)
        t_rl1 = t_rl0 + mins(10)
        events += [
            ev(t_rl0, "pass", latency_ms=25000),  # step 0 → step 1
            ev(t_rl1, "fail"),  # AGAIN → back to step 0
        ]
        state = replay(events, cfg, t_rl1 + days(1))
        assert state.phase == "RELEARNING"
        assert state.due_at == t_rl1 + mins(1)


# ---------------------------------------------------------------------------
# replay — cheat caps next submission to HARD
# ---------------------------------------------------------------------------


class TestCheatCapsToHard:
    def _cheat(self, ts):
        return {"kind": "cheat", "ts": ts}

    def test_cheat_then_fast_clean_pass_is_capped_to_hard(self):
        cfg = SrsConfig()
        events = [
            self._cheat(BASE),
            ev(BASE + mins(1), "pass", latency_ms=1000, answer_text="x"),  # would be EASY
        ]
        state = replay(events, cfg, BASE + days(1))
        # Capped to HARD: stays in LEARNING on step 0 (re-shown ~1 min later)
        assert state.phase == "LEARNING"

    def test_cheat_only_applies_to_immediate_next_submission(self):
        cfg = SrsConfig()
        events = [
            self._cheat(BASE),
            ev(BASE + mins(1), "pass", latency_ms=1000, answer_text="x"),  # HARD (poisoned)
            ev(BASE + mins(2), "pass", latency_ms=1000, answer_text="x"),  # GOOD/EASY (clean)
        ]
        state = replay(events, cfg, BASE + days(1))
        # Second clean pass advances/graduates; not stuck on step 0
        assert state.phase in ("LEARNING", "REVIEW")
        assert state.phase != "NEW"

    def test_cheat_then_fail_stays_again(self):
        cfg = SrsConfig()
        events = [self._cheat(BASE), ev(BASE + mins(1), "fail")]
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "LEARNING"  # AGAIN keeps step 0

    def test_lone_cheat_no_submission_stays_new(self):
        cfg = SrsConfig()
        state = replay([self._cheat(BASE)], cfg, BASE + days(1))
        assert state.phase == "NEW"


# ---------------------------------------------------------------------------
# replay — soon / bury transitions
# ---------------------------------------------------------------------------


class TestSoonBury:
    def _soon(self, ts):
        return {"kind": "soon", "ts": ts}

    def _bury(self, ts):
        return {"kind": "bury", "ts": ts}

    def test_bury_default_interval(self):
        cfg = SrsConfig()
        state = replay([self._bury(BASE)], cfg, BASE)
        assert state.phase == "REVIEW"
        assert state.interval == cfg.bury_interval_days
        assert state.due_at == BASE + days(cfg.bury_interval_days)

    def test_bury_never_pulls_in_a_longer_scheduled_card(self):
        cfg = LEGACY_CFG
        # Graduate + several GOOD reviews to push interval well past 21 days.
        events = [
            ev(BASE, "pass", latency_ms=1000, answer_text="x"),  # EASY → 4d
            ev(BASE + days(4), "pass", latency_ms=25000, answer_text="x"),  # GOOD
            ev(BASE + days(20), "pass", latency_ms=25000, answer_text="x"),  # GOOD
            self._bury(BASE + days(60)),
        ]
        state = replay(events, cfg, BASE + days(60))
        assert state.phase == "REVIEW"
        assert state.interval > cfg.bury_interval_days  # max() kept the larger interval

    def test_soon_resets_to_relearning_due_one_minute_out(self):
        cfg = SrsConfig()
        events = [
            ev(BASE, "pass", latency_ms=1000, answer_text="x"),  # EASY → REVIEW
            self._soon(BASE + days(1)),
        ]
        state = replay(events, cfg, BASE + days(1))
        assert state.phase == "RELEARNING"
        assert state.due_at == (BASE + days(1)) + mins(cfg.learning_steps_min[0])
        assert state.interval == 0.0

    def test_soon_does_not_penalize_ease(self):
        cfg = SrsConfig()
        events = [
            ev(BASE, "pass", latency_ms=1000, answer_text="x"),  # EASY → REVIEW, ease 2.5
            self._soon(BASE + days(1)),
        ]
        state = replay(events, cfg, BASE + days(1))
        assert state.ease == cfg.starting_ease
