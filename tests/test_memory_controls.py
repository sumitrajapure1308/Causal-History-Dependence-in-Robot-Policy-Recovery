"""Unit Tests for Explicit Memory Controls and State Invariance.

Validates the implementation of explicit memory controls:
1. test_policy_memory_save_and_restore: Bitwise exact memory state get/set.
2. test_policy_memory_reset: Explicit zeroing of hidden state and clear buffers.
3. test_environment_state_bitwise_restored: Physical state matching error <= 1e-10 m.
4. test_action_prefix_replay_determinism: Exact reproducibility of unrolled memory.
5. test_remaining_horizon_preserved: Invariant task horizon across conditions.
6. test_four_memory_conditions_setup: Correct configuration of Conditions A, B, C, D.
7. test_no_memory_leakage_across_evaluations: Isolation between successive evaluations.
"""

from __future__ import annotations

import os
import sys
import copy
import numpy as np
import pytest
import torch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.history_gru import HistoryGRUPolicy
from causal_history_recovery.policies.recovery_augmented_gru import RecoveryAugmentedGRUPolicy
from causal_history_recovery.policies.reactive_mlp import ReactiveMLPPolicy
from causal_history_recovery.counterfactuals.condition_generator import (
    ConditionGenerator,
    COND_REPLAY_PRESERVED,
    COND_INJECT_PRESERVED,
    COND_INJECT_RESET,
    COND_INJECT_ALTERNATIVE,
)


@pytest.fixture
def env():
    """Create a standard test environment."""
    return PushTargetEnv()


@pytest.fixture
def gru_policy():
    """Create a standard HistoryGRU policy."""
    cfg = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "history_window": 5,
        "hidden_dim": 32,
    }
    return HistoryGRUPolicy(cfg)


@pytest.fixture
def rec_policy():
    """Create a standard RecoveryAugmentedGRU policy."""
    cfg = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "history_window": 5,
        "hidden_dim": 32,
    }
    return RecoveryAugmentedGRUPolicy(cfg)


@pytest.fixture
def mlp_policy():
    """Create a ReactiveMLP policy."""
    cfg = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "hidden_dims": [64, 64],
    }
    return ReactiveMLPPolicy(cfg)


def test_policy_memory_save_and_restore(gru_policy, rec_policy, mlp_policy):
    """Verify bitwise exact memory get/set across policy architectures."""
    # 1. Test HistoryGRUPolicy
    obs0 = np.random.randn(20).astype(np.float32)
    gru_policy.reset(obs0)
    for _ in range(5):
        gru_policy.act(np.random.randn(20).astype(np.float32))

    mem_state = gru_policy.get_memory_state()
    assert gru_policy.has_recurrent_memory() is True
    assert "hidden_state" in mem_state
    assert "obs_buffer" in mem_state
    assert "action_buffer" in mem_state
    h_saved = mem_state["hidden_state"].numpy().copy()

    # Mutate policy state
    gru_policy.act(np.random.randn(20).astype(np.float32))
    assert not np.allclose(gru_policy.get_memory_state()["hidden_state"].numpy(), h_saved)

    # Restore memory state
    gru_policy.set_memory_state(mem_state)
    h_restored = gru_policy.get_memory_state()["hidden_state"].numpy()
    assert np.allclose(h_saved, h_restored, atol=1e-12)

    # 2. Test RecoveryAugmentedGRUPolicy
    rec_policy.reset(obs0)
    for _ in range(5):
        rec_policy.act(np.random.randn(20).astype(np.float32))

    rec_mem = rec_policy.get_memory_state()
    assert rec_policy.has_recurrent_memory() is True
    assert "hidden_state" in rec_mem
    assert "contact_buffer" in rec_mem
    assert "deviation_detected" in rec_mem
    h_rec_saved = rec_mem["hidden_state"].numpy().copy()

    rec_policy.set_memory_state(rec_mem)
    h_rec_restored = rec_policy.get_memory_state()["hidden_state"].numpy()
    assert np.allclose(h_rec_saved, h_rec_restored, atol=1e-12)

    # 3. Test ReactiveMLPPolicy (stateless)
    mlp_policy.reset(obs0)
    assert mlp_policy.has_recurrent_memory() is False
    assert mlp_policy.get_memory_state()["type"] == "memoryless"
    assert mlp_policy.get_memory_state()["hidden_state"] is None
    mlp_policy.set_memory_state({})  # Safe no-op


def test_policy_memory_reset(gru_policy):
    """Verify reset_memory strictly zeroes recurrent hidden states."""
    obs0 = np.random.randn(20).astype(np.float32)
    gru_policy.reset(obs0)
    for _ in range(8):
        gru_policy.act(np.random.randn(20).astype(np.float32))

    h_active = gru_policy.get_hidden_state()
    assert torch.norm(h_active).item() > 1e-4

    # Explicit reset
    gru_policy.reset_memory(obs0)
    h_reset = gru_policy.get_hidden_state()
    assert torch.norm(h_reset).item() == 0.0

    # Verify action buffer is zeroed
    mem_state = gru_policy.get_memory_state()
    for act in mem_state["action_buffer"]:
        assert np.allclose(act, np.zeros(3), atol=1e-12)


def test_environment_state_bitwise_restored(env, gru_policy):
    """Verify physical state snapshot restoration is bitwise identical (D <= 1e-10 m)."""
    env.reset(seed=123)
    prefix_actions = [np.array([0.002, 0.0, 0.0]) for _ in range(12)]
    for act in prefix_actions:
        env.step(act)

    target_snap = env.get_state_snapshot()
    cond_gen = ConditionGenerator(env)

    conditions = [
        COND_REPLAY_PRESERVED,
        COND_INJECT_PRESERVED,
        COND_INJECT_RESET,
        COND_INJECT_ALTERNATIVE,
    ]

    for cond in conditions:
        setup_info = cond_gen.prepare_condition_rollout(
            condition=cond,
            policy=gru_policy,
            source_snapshot=target_snap,
            action_prefix=prefix_actions,
            seed=123,
        )

        current_snap = env.get_state_snapshot()
        qpos_diff = np.linalg.norm(current_snap.qpos - target_snap.qpos)
        qvel_diff = np.linalg.norm(current_snap.qvel - target_snap.qvel)

        assert qpos_diff <= 1e-10, f"Condition {cond} failed qpos match: diff={qpos_diff}"
        assert qvel_diff <= 1e-10, f"Condition {cond} failed qvel match: diff={qvel_diff}"
        assert setup_info["state_matching_error"] <= 1e-10


def test_action_prefix_replay_determinism(env, gru_policy):
    """Verify action prefix unrolling yields deterministic hidden state and physical state."""
    prefix_actions = [np.array([0.003, 0.001, 0.0]) for _ in range(15)]
    cond_gen = ConditionGenerator(env)

    # First unroll
    mem_1 = cond_gen.unroll_policy_memory_on_prefix(gru_policy, seed=42, action_prefix=prefix_actions)
    h_1 = mem_1["hidden_state"].numpy()

    # Second unroll
    mem_2 = cond_gen.unroll_policy_memory_on_prefix(gru_policy, seed=42, action_prefix=prefix_actions)
    h_2 = mem_2["hidden_state"].numpy()

    assert np.allclose(h_1, h_2, atol=1e-12)


def test_remaining_horizon_preserved(env, gru_policy):
    """Verify remaining task horizon is strictly identical across all conditions."""
    env.reset(seed=99)
    prefix_actions = [np.array([0.002, 0.0, 0.0]) for _ in range(20)]
    for act in prefix_actions:
        env.step(act)
    target_snap = env.get_state_snapshot()
    expected_remaining_horizon = env.remaining_horizon

    cond_gen = ConditionGenerator(env)
    for cond in [COND_REPLAY_PRESERVED, COND_INJECT_PRESERVED, COND_INJECT_RESET, COND_INJECT_ALTERNATIVE]:
        setup_info = cond_gen.prepare_condition_rollout(
            condition=cond,
            policy=gru_policy,
            source_snapshot=target_snap,
            action_prefix=prefix_actions,
            seed=99,
        )
        assert env.remaining_horizon == expected_remaining_horizon
        assert setup_info["remaining_horizon"] == expected_remaining_horizon


def test_four_memory_conditions_setup(env, gru_policy):
    """Verify exact semantic configuration of the four memory conditions."""
    env.reset(seed=77)
    prefix_actions = [np.array([0.002, 0.001, 0.0]) for _ in range(15)]
    for act in prefix_actions:
        env.step(act)
    target_snap = env.get_state_snapshot()

    cond_gen = ConditionGenerator(env)

    # Condition A: Replay with preserved memory
    setup_a = cond_gen.prepare_condition_rollout(
        condition=COND_REPLAY_PRESERVED,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=77,
    )
    assert setup_a["execution_mode"] == "replay"
    assert setup_a["hidden_state_status"] == "preserved"
    h_norm_a = setup_a["initial_hidden_norm"]
    assert h_norm_a > 1e-4

    # Condition B: Injected matched state with preserved memory
    setup_b = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_PRESERVED,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=77,
    )
    assert setup_b["execution_mode"] == "injection"
    assert setup_b["hidden_state_status"] == "preserved"
    h_norm_b = setup_b["initial_hidden_norm"]
    assert np.isclose(h_norm_a, h_norm_b, atol=1e-5)

    # Condition C: Injected matched state with reset memory
    setup_c = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_RESET,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=77,
    )
    assert setup_c["execution_mode"] == "injection"
    assert setup_c["hidden_state_status"] == "reset"
    assert setup_c["initial_hidden_norm"] == 0.0
    h_c = gru_policy.get_hidden_state()
    assert torch.norm(h_c).item() == 0.0

    # Condition D: Injected matched state with alternative compatible memory
    setup_d = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_ALTERNATIVE,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=77,
    )
    assert setup_d["execution_mode"] == "injection"
    assert setup_d["hidden_state_status"] == "alternative"
    assert setup_d["initial_hidden_norm"] > 1e-4


def test_no_memory_leakage_across_evaluations(env, gru_policy):
    """Verify that successive rollouts do not leak memory states between runs."""
    env.reset(seed=88)
    prefix_actions = [np.array([0.002, 0.0, 0.0]) for _ in range(10)]
    for act in prefix_actions:
        env.step(act)
    target_snap = env.get_state_snapshot()
    cond_gen = ConditionGenerator(env)

    # 1. Run preserved memory setup
    setup_b = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_PRESERVED,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=88,
    )
    assert setup_b["initial_hidden_norm"] > 1e-4

    # 2. Immediately run reset memory setup on SAME policy instance
    setup_c = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_RESET,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=88,
    )
    assert setup_c["initial_hidden_norm"] == 0.0
    assert torch.norm(gru_policy.get_hidden_state()).item() == 0.0

    # 3. Immediately run preserved memory setup again
    setup_b2 = cond_gen.prepare_condition_rollout(
        condition=COND_INJECT_PRESERVED,
        policy=gru_policy,
        source_snapshot=target_snap,
        action_prefix=prefix_actions,
        seed=88,
    )
    assert np.isclose(setup_b2["initial_hidden_norm"], setup_b["initial_hidden_norm"], atol=1e-6)
