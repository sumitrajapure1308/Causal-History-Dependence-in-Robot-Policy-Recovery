"""Unit Tests for ConditionGenerator.

Validates:
1. Preparation of Condition B0 (prefix replay, preserved history).
2. Preparation of Condition B1 (action ablated).
3. Preparation of Condition B2 (observation ablated).
4. Preparation of Condition B3 (hidden state reset).
5. Preparation of Condition B4 (fully ablated).
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
from causal_history_recovery.policies.history_gru import HistoryGRUPolicy
from causal_history_recovery.counterfactuals.condition_generator import ConditionGenerator


def test_condition_generator_all_conditions():
    """Verify condition preparation across B0, B1, B2, B3, B4."""
    env = PushTargetEnv()
    cond_gen = ConditionGenerator(env)

    policy_cfg = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "history_window": 5,
        "hidden_dim": 32,
    }
    policy = HistoryGRUPolicy(policy_cfg)

    # Induce small prefix
    env.reset(seed=42)
    actions = [np.array([0.003, 0.0, 0.0]) for _ in range(10)]
    for a in actions:
        env.step(a)
    source_snap = env.get_state_snapshot()

    # Test B0
    prep_b0 = cond_gen.prepare_condition_rollout(
        condition="B0",
        policy=policy,
        source_snapshot=source_snap,
        action_prefix=actions,
        seed=42,
    )
    assert prep_b0["condition"] == "B0"
    assert prep_b0["state_matching_error"] < 1e-10
    assert prep_b0["obs_history_status"] == "preserved"

    # Test B1
    prep_b1 = cond_gen.prepare_condition_rollout(
        condition="B1",
        policy=policy,
        source_snapshot=source_snap,
        action_prefix=actions,
        seed=42,
    )
    assert prep_b1["condition"] == "B1"
    assert prep_b1["action_history_status"] == "ablated"

    # Test B2
    prep_b2 = cond_gen.prepare_condition_rollout(
        condition="B2",
        policy=policy,
        source_snapshot=source_snap,
        action_prefix=actions,
        seed=42,
    )
    assert prep_b2["condition"] == "B2"
    assert prep_b2["obs_history_status"] == "ablated"

    # Test B3
    prep_b3 = cond_gen.prepare_condition_rollout(
        condition="B3",
        policy=policy,
        source_snapshot=source_snap,
        action_prefix=actions,
        seed=42,
    )
    assert prep_b3["condition"] == "B3"
    assert prep_b3["hidden_state_status"] == "reset"

    # Test B4
    prep_b4 = cond_gen.prepare_condition_rollout(
        condition="B4",
        policy=policy,
        source_snapshot=source_snap,
        action_prefix=actions,
        seed=42,
    )
    assert prep_b4["condition"] == "B4"
    assert prep_b4["obs_history_status"] == "ablated"
    assert prep_b4["action_history_status"] == "ablated"
    assert prep_b4["hidden_state_status"] == "reset"
    assert prep_b4["state_matching_error"] < 1e-10

