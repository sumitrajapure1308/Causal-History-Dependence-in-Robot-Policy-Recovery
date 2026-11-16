"""Unit Tests for Policy Suite and Registry.

Validates:
1. ReactiveMLPPolicy output dimensions, action bounds, and statelessness.
2. HistoryGRUPolicy sliding window buffer, recurrent hidden state manipulations, and selective ablation.
3. Policy registry factory creation and checkpoint loading.
"""

from __future__ import annotations

import os
import sys
import tempfile
import numpy as np
import pytest
import torch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.policies.reactive_mlp import ReactiveMLPPolicy
from causal_history_recovery.policies.history_gru import HistoryGRUPolicy
from causal_history_recovery.policies.policy_registry import (
    create_policy,
    get_policy_class,
    list_registered_policies,
    load_policy,
)


def test_reactive_mlp_policy():
    """Verify ReactiveMLPPolicy executes deterministically and respects action bounds."""
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "hidden_dims": [64, 64],
        "activation": "relu",
        "device": "cpu",
    }
    policy = ReactiveMLPPolicy(config)

    obs = np.random.randn(20).astype(np.float32)
    act1 = policy.act(obs, deterministic=True)
    act2 = policy.act(obs, deterministic=True)

    assert act1.shape == (3,)
    assert np.allclose(act1, act2), "Deterministic evaluation produced divergent actions!"
    assert np.all(act1 >= -0.02) and np.all(act1 <= 0.02), "Action exceeded action_limit bounds!"

    # Verify statelessness
    assert policy.get_hidden_state() is None
    policy.reset()
    policy.reset_hidden_state()

    # Test serialization
    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        tmp_path = f.name
    try:
        policy.save(tmp_path)
        loaded = ReactiveMLPPolicy(config)
        loaded.load(tmp_path)
        act_loaded = loaded.act(obs, deterministic=True)
        assert np.allclose(act1, act_loaded, atol=1e-6)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_history_gru_policy():
    """Verify HistoryGRUPolicy buffer updates, recurrent state transitions, and ablation."""
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "history_window": 5,
        "hidden_dim": 64,
        "num_layers": 1,
        "device": "cpu",
    }
    policy = HistoryGRUPolicy(config)

    obs0 = np.ones(20, dtype=np.float32)
    policy.reset(obs0)

    # Initial history summary
    summary = policy.get_history_summary()
    assert summary["obs_buffered"] == 5
    assert summary["actions_buffered"] == 5

    # Step forward 3 times
    for i in range(3):
        obs_i = np.full(20, fill_value=i, dtype=np.float32)
        act_i = policy.act(obs_i, deterministic=True)
        assert act_i.shape == (3,)
        assert np.all(act_i >= -0.02) and np.all(act_i <= 0.02)

    # Inspect hidden state
    h = policy.get_hidden_state()
    assert h is not None
    assert h.shape == (1, 1, 64)
    assert torch.norm(h).item() > 0.0

    # Test hidden state reset (Condition B3)
    policy.reset_hidden_state()
    h_reset = policy.get_hidden_state()
    assert torch.norm(h_reset).item() == 0.0

    # Test observation and action ablation (Condition B4)
    cur_obs = np.full(20, 99.0, dtype=np.float32)
    policy.ablate_history(cur_obs, ablate_obs=True, ablate_act=True)
    assert np.all(policy.obs_buffer[-1] == 99.0)
    assert np.all(policy.action_buffer[-1] == 0.0)

    # Test serialization
    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        tmp_path = f.name
    try:
        policy.save(tmp_path)
        loaded = HistoryGRUPolicy(config)
        loaded.load(tmp_path)
        policy.reset(obs0)
        loaded.reset(obs0)
        a1 = policy.act(obs0)
        a2 = loaded.act(obs0)
        assert np.allclose(a1, a2, atol=1e-6)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_policy_registry():
    """Verify registry lists policies and instantiates them correctly."""
    registered = list_registered_policies()
    assert "reactive_mlp" in registered
    assert "history_gru" in registered
    assert "recovery_augmented_mlp" in registered
    assert "recovery_augmented_gru" in registered

    mlp_cls = get_policy_class("recovery_augmented_mlp")
    assert mlp_cls.__name__ == "RecoveryAugmentedMLPPolicy"

    policy = create_policy("recovery_augmented_mlp", {"obs_dim": 20, "action_dim": 3, "action_limit": 0.02})
    assert policy is not None


def test_recovery_augmented_mlp():
    """Verify RecoveryAugmentedMLPPolicy feature augmentation and action bounds."""
    from causal_history_recovery.policies.recovery_augmented_mlp import RecoveryAugmentedMLPPolicy
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "hidden_dims": [64, 64],
        "device": "cpu",
    }
    policy = RecoveryAugmentedMLPPolicy(config)
    obs = np.random.randn(20).astype(np.float32)
    act = policy.act(obs, deterministic=True, remaining_horizon=0.5)

    assert act.shape == (3,)
    assert np.all(act >= -0.02) and np.all(act <= 0.02)


def test_recovery_augmented_gru():
    """Verify RecoveryAugmentedGRUPolicy token handling and counterfactual ablations."""
    from causal_history_recovery.policies.recovery_augmented_gru import RecoveryAugmentedGRUPolicy
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "action_limit": 0.02,
        "history_window": 5,
        "hidden_dim": 64,
        "num_layers": 1,
        "device": "cpu",
    }
    policy = RecoveryAugmentedGRUPolicy(config)
    obs = np.random.randn(20).astype(np.float32)
    policy.reset(obs)
    act = policy.act(obs, deterministic=True, remaining_horizon=0.5, contact_present=1.0)

    assert act.shape == (3,)
    assert np.all(act >= -0.02) and np.all(act <= 0.02)
    assert policy.get_hidden_state() is not None

    # Test B4 condition ablation
    policy.apply_counterfactual_condition("B4", obs)
    assert np.allclose(policy.get_hidden_state().cpu().numpy(), 0.0)


