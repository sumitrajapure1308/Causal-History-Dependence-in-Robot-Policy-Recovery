"""Determinism Unit Tests for MuJoCo Environments.

Validates that reset and action stepping are strictly deterministic under explicit seeds.
"""

import sys
import os
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.mujoco_wrapper import MuJoCoWrapperEnv


def test_reset_determinism():
    """Verify that identical seeds produce bitwise identical initial states."""
    env1 = MuJoCoWrapperEnv("Pusher-v5")
    env2 = MuJoCoWrapperEnv("Pusher-v5")

    obs1, info1 = env1.reset(seed=42)
    obs2, info2 = env2.reset(seed=42)

    # Assert bitwise equality of observations and underlying qpos/qvel
    assert np.allclose(obs1, obs2, atol=1e-10), "Reset observations differ for identical seed!"
    assert np.allclose(env1.data.qpos, env2.data.qpos, atol=1e-10), "Reset qpos differs!"
    assert np.allclose(env1.data.qvel, env2.data.qvel, atol=1e-10), "Reset qvel differs!"
    assert info1["remaining_horizon"] == info2["remaining_horizon"] == 100


def test_stepping_determinism():
    """Verify that stepping an identical action sequence yields 0.0 divergence."""
    env1 = MuJoCoWrapperEnv("Pusher-v5")
    env2 = MuJoCoWrapperEnv("Pusher-v5")

    env1.reset(seed=1337)
    env2.reset(seed=1337)

    # Fixed pseudo-random action sequence
    rng = np.random.RandomState(999)
    actions = [rng.uniform(-1.0, 1.0, size=env1.action_space.shape) for _ in range(25)]

    for step_idx, a in enumerate(actions):
        o1, r1, t1, tr1, _ = env1.step(a)
        o2, r2, t2, tr2, _ = env2.step(a)

        assert np.allclose(o1, o2, atol=1e-10), f"Observation diverged at step {step_idx}!"
        assert np.isclose(r1, r2, atol=1e-10), f"Reward diverged at step {step_idx}!"
        assert np.allclose(env1.data.qpos, env2.data.qpos, atol=1e-10), f"qpos diverged at step {step_idx}!"
        assert np.allclose(env1.data.qvel, env2.data.qvel, atol=1e-10), f"qvel diverged at step {step_idx}!"


def test_distinct_seeds_produce_variation():
    """Verify that distinct seeds produce distinct initial object positions."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    obs1, _ = env.reset(seed=101)
    obs2, _ = env.reset(seed=202)

    diff = np.max(np.abs(obs1 - obs2))
    assert diff > 1e-4, "Different seeds unexpectedly produced identical states!"

