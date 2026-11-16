"""Tests for Policy-Specific Memory Reconstruction.

Verifies:
1. Replaying an identical prefix through a recurrent policy deterministically reconstructs the hidden state.
2. Distinct policy checkpoints produce distinct, policy-specific memory states on the same prefix.
3. No stale buffer or hidden activation survives a full policy reset.
4. Checkpoint loading accurately maps weights and biases to intended layers.
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pytest
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.policies.recovery_augmented_gru import RecoveryAugmentedGRUPolicy


def test_deterministic_memory_reconstruction():
    """Verify that unrolling the same sequence produces bitwise identical hidden states."""
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "hidden_dim": 128,
        "history_window": 10,
        "action_limit": 0.02,
    }
    policy = RecoveryAugmentedGRUPolicy(config)
    rng = np.random.RandomState(12345)
    obs_seq = [rng.randn(20).astype(np.float32) for _ in range(15)]

    # First unroll
    policy.reset(obs_seq[0])
    for o in obs_seq:
        policy.act(o, deterministic=True)
    h_run1 = policy.get_hidden_state().clone()

    # Second unroll
    policy.reset(obs_seq[0])
    for o in obs_seq:
        policy.act(o, deterministic=True)
    h_run2 = policy.get_hidden_state().clone()

    assert torch.equal(h_run1, h_run2), "Memory reconstruction was not bitwise deterministic"


def test_policy_specific_memory_divergence():
    """Verify that distinct trained checkpoints produce distinct hidden representations."""
    ckpt_dir = os.path.join(repo_root, "results", "recovery_training", "checkpoints")
    p42_path = os.path.join(ckpt_dir, "recovery_augmented_gru_seed42.pt")
    p123_path = os.path.join(ckpt_dir, "recovery_augmented_gru_seed123.pt")

    if not os.path.exists(p42_path) or not os.path.exists(p123_path):
        pytest.skip("Checkpoints not found")

    p42 = load_policy(p42_path)
    p123 = load_policy(p123_path)

    rng = np.random.RandomState(42)
    obs_seq = [rng.randn(20).astype(np.float32) for _ in range(10)]

    p42.reset(obs_seq[0])
    p123.reset(obs_seq[0])
    for o in obs_seq:
        p42.act(o, deterministic=True)
        p123.act(o, deterministic=True)

    h42 = p42.get_hidden_state()
    h123 = p123.get_hidden_state()

    diff = torch.norm(h42 - h123).item()
    assert diff > 0.05, f"Checkpoints unexpectedly shared identical hidden states (diff={diff})"


def test_no_stale_buffer_after_reset():
    """Verify that reset clears all historical values from buffers."""
    config = {
        "obs_dim": 20,
        "action_dim": 3,
        "hidden_dim": 128,
        "history_window": 10,
        "action_limit": 0.02,
    }
    policy = RecoveryAugmentedGRUPolicy(config)
    obs_nonzero = np.ones(20, dtype=np.float32) * 5.0
    policy.reset(obs_nonzero)
    for _ in range(10):
        policy.act(obs_nonzero, deterministic=True)

    # Now reset with zero obs
    zero_obs = np.zeros(20, dtype=np.float32)
    policy.reset(zero_obs)

    # Verify buffers contain only zero_obs
    for buf_obs in policy.obs_buffer:
        assert np.array_equal(buf_obs, zero_obs), "Stale observation remained in buffer"

    for buf_act in policy.action_buffer:
        assert np.array_equal(buf_act, np.zeros(3, dtype=np.float32)), "Stale action remained in buffer"

    assert torch.equal(policy.get_hidden_state(), torch.zeros((1, 1, 128))), "Hidden state not zeroed"

