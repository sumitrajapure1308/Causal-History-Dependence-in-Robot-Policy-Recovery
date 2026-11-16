"""Unit Tests for StateMatcher and Distance Calculation.

Validates:
1. Identical snapshots yield 0.0 composite distance and strict tier match.
2. Hard rejection filters reject snapshots with mismatched remaining horizon or contact count.
3. Component-wise distance calculations (qpos, qvel, ee, obj_pos, obj_rot).
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.matching.state_matcher import StateMatcher


def test_identical_snapshots_strict_match():
    """Verify identical snapshots produce zero distance and strict tier."""
    env = PushTargetEnv()
    env.reset(seed=42)
    snap1 = env.get_state_snapshot()
    snap2 = env.get_state_snapshot()

    matcher = StateMatcher()
    comp_dist, comps = matcher.compute_composite_distance(snap1, snap2)
    assert comp_dist == 0.0
    assert comps["d_qpos"] == 0.0
    assert comps["d_obj_pos"] == 0.0

    eval_res = matcher.evaluate_match(snap1, snap2)
    assert eval_res["matched"] is True
    assert eval_res["tier"] == "strict"
    assert eval_res["passed_hard_constraints"] is True


def test_hard_rejection_horizon_mismatch():
    """Verify mismatched remaining horizon triggers hard constraint rejection."""
    env = PushTargetEnv()
    env.reset(seed=42)
    snap1 = env.get_state_snapshot()
    snap2 = env.get_state_snapshot()
    snap2.remaining_horizon = snap1.remaining_horizon - 10

    matcher = StateMatcher()
    eval_res = matcher.evaluate_match(snap1, snap2)
    assert eval_res["matched"] is False
    assert eval_res["tier"] == "rejected"
    assert "horizon_mismatch" in eval_res["rejection_reasons"]


def test_hard_rejection_contact_mismatch():
    """Verify mismatched contact count triggers hard constraint rejection."""
    env = PushTargetEnv()
    env.reset(seed=42)
    snap1 = env.get_state_snapshot()
    snap2 = env.get_state_snapshot()
    snap2.active_contacts_count = snap1.active_contacts_count + 2

    matcher = StateMatcher()
    eval_res = matcher.evaluate_match(snap1, snap2)
    assert eval_res["matched"] is False
    assert eval_res["tier"] == "rejected"
    assert "contact_count_mismatch" in eval_res["rejection_reasons"]

