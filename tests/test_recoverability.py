"""Unit Tests for Recoverability Specification and Privileged Oracle Filter.

Validates:
1. Privileged oracle controller achieves binary recovery (R_oracle = 1) from recoverable off-center slip.
2. Horizon-deficient failure states (< 35 steps remaining) are rejected (R_oracle = 0).
3. Kinematically unreachable states (> 0.35m) are rejected.
4. Table departure states (z < 0.015m) are rejected.
5. Scenario admission pipeline excludes unrecoverable cases from the benchmark denominator.
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
from causal_history_recovery.controllers.privileged_oracle import PrivilegedOracleController


def test_privileged_oracle_solves_recoverable_failure():
    """Verify oracle recovers from an off-center slip failure satisfying all 8 admission criteria."""
    env = PushTargetEnv(max_horizon=150)
    env.reset(seed=42)

    # 1. Forward push
    for _ in range(25):
        env.step(np.array([0.004, 0.0, 0.0]))

    # 2. Lateral shift to induce off-center slip
    for _ in range(5):
        env.step(np.array([0.0, 0.003, 0.0]))
    for _ in range(12):
        env.step(np.array([0.004, 0.0, 0.0]))

    snap_fail = env.get_state_snapshot()

    oracle = PrivilegedOracleController()
    admitted, audit = oracle.verify_scenario_recoverability(env, snap_fail)

    assert admitted is True, f"Scenario was not admitted: {audit}"
    assert audit["checks"]["physical_deviation"] is True
    assert audit["checks"]["kinematic_reachability"] is True
    assert audit["checks"]["horizon_sufficiency"] is True
    assert audit["checks"]["oracle_recovery"] is True
    assert audit["execution"]["success"] is True


def test_insufficient_horizon_rejected():
    """Verify scenarios with < 35 steps remaining are rejected without penalizing policy."""
    env = PushTargetEnv(max_horizon=150)
    env.reset(seed=42)

    snap = env.get_state_snapshot()
    # Force object into deviated state
    snap.qpos[4] = 0.03  # lateral drift
    snap.remaining_horizon = 15  # below 35 step threshold

    oracle = PrivilegedOracleController()
    admitted, audit = oracle.verify_scenario_recoverability(env, snap)

    assert admitted is False
    assert audit["checks"]["horizon_sufficiency"] is False


def test_out_of_bounds_state_rejected():
    """Verify scenarios where object is beyond physical reach are rejected."""
    env = PushTargetEnv(max_horizon=150)
    env.reset(seed=42)

    snap = env.get_state_snapshot()
    snap.qpos[3] = 0.40  # outside reach bounds [-0.35, 0.35]

    oracle = PrivilegedOracleController()
    admitted, audit = oracle.verify_scenario_recoverability(env, snap)

    assert admitted is False
    assert audit["checks"]["kinematic_reachability"] is False


def test_table_fall_rejected():
    """Verify scenarios where object has fallen off the table are rejected."""
    env = PushTargetEnv(max_horizon=150)
    env.reset(seed=42)

    snap = env.get_state_snapshot()
    snap.qpos[4] = 0.03
    snap.qpos[5] = 0.005  # below table surface clearance (0.015m)

    oracle = PrivilegedOracleController()
    admitted, audit = oracle.verify_scenario_recoverability(env, snap)

    assert admitted is False
    assert audit["checks"]["no_catastrophe"] is False


def test_exclusion_from_recovery_denominator():
    """Verify that unrecoverable scenarios do not contribute to benchmark denominator."""
    env = PushTargetEnv(max_horizon=150)
    oracle = PrivilegedOracleController()

    candidate_scenarios = []

    # Scenario A: Valid recoverable scenario
    env.reset(seed=42)
    for _ in range(25):
        env.step(np.array([0.004, 0.0, 0.0]))
    for _ in range(5):
        env.step(np.array([0.0, 0.003, 0.0]))
    for _ in range(12):
        env.step(np.array([0.004, 0.0, 0.0]))
    candidate_scenarios.append(env.get_state_snapshot())

    # Scenario B: Unrecoverable scenario (insufficient steps)
    snap_unrec = env.get_state_snapshot()
    snap_unrec.remaining_horizon = 10
    candidate_scenarios.append(snap_unrec)

    # Filter candidate scenarios
    admitted_scenarios = []
    for snap in candidate_scenarios:
        admitted, _ = oracle.verify_scenario_recoverability(env, snap)
        if admitted:
            admitted_scenarios.append(snap)

    # Denominator must exclude Scenario B
    assert len(candidate_scenarios) == 2
    assert len(admitted_scenarios) == 1
    assert admitted_scenarios[0].remaining_horizon >= 35

