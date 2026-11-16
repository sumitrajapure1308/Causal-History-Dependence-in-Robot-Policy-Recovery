"""Unit tests for Paired Scenario Generation and 15-Point Validation."""

import os
import sys
import numpy as np
import pytest
import torch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.policies.history_gru import HistoryGRUPolicy
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.counterfactuals.paired_scenario_generator import PairedScenarioGenerator


@pytest.fixture
def env():
    return PushTargetEnv()


@pytest.fixture
def policy():
    ckpt_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "models", "checkpoints", "history_gru_best.pt"
    ))
    if os.path.exists(ckpt_path):
        return load_policy(ckpt_path, device="cpu")
    else:
        cfg = {
            "obs_dim": 20,
            "action_dim": 3,
            "hidden_dim": 128,
            "history_window": 10,
            "num_layers": 1,
        }
        return HistoryGRUPolicy(cfg)


def test_generator_initialization(env):
    gen = PairedScenarioGenerator(env)
    assert gen.env is not None
    assert gen.oracle is not None
    assert gen.condition_gen is not None


def test_sample_source_failure_detection(env, policy):
    gen = PairedScenarioGenerator(env)
    source = gen.sample_source_failure(
        policy=policy,
        seed=42,
        severity_tier="medium",
        offset_y=0.016,
        perturb_step=25,
        direction=1.0,
        yaw_threshold_deg=10.0,
        drift_threshold_m=0.012,
    )
    assert source is not None
    assert source["deviation_step"] >= 25
    assert source["peak_yaw_deg"] >= 10.0
    assert source["candidate_snapshot"] is not None
    assert len(source["action_history"]) >= 25


def test_paired_scenario_conditions_and_matching(env, policy):
    gen = PairedScenarioGenerator(env)
    source = gen.sample_source_failure(
        policy=policy,
        seed=77,
        severity_tier="medium",
        offset_y=0.016,
        perturb_step=25,
        yaw_threshold_deg=10.0,
        drift_threshold_m=0.012,
    )
    assert source is not None

    scenario = gen.generate_paired_scenario(source, policy, policy_id="history_gru")
    assert "conditions" in scenario
    for cond_name in ["B0", "B1", "B2", "B3", "B4"]:
        assert cond_name in scenario["conditions"]
        c_data = scenario["conditions"][cond_name]
        assert c_data["state_matching_error"] <= 1e-4
        assert c_data["remaining_horizon"] == scenario["remaining_horizon"]

    # Verify B3 and B4 hidden states are zero
    assert scenario["conditions"]["B3"]["hidden_norm"] == 0.0
    assert scenario["conditions"]["B4"]["hidden_norm"] == 0.0


def test_15_point_validation_rules(env, policy):
    gen = PairedScenarioGenerator(env)
    source = gen.sample_source_failure(
        policy=policy,
        seed=77,
        severity_tier="medium",
        offset_y=0.016,
        perturb_step=25,
        yaw_threshold_deg=10.0,
        drift_threshold_m=0.012,
    )
    assert source is not None

    scenario = gen.generate_paired_scenario(source, policy, policy_id="history_gru")
    val_report = scenario["validation_report"]
    assert "rules" in val_report
    assert val_report["total_rules_count"] == 15
    # Check that critical rules passed
    assert val_report["rules"]["1_source_failure_plausible"] is True
    assert val_report["rules"]["3_physical_state_valid"] is True
    assert val_report["rules"]["7_goal_state_preserved"] is True
    assert val_report["rules"]["8_horizon_preserved"] is True
    assert val_report["rules"]["9_state_matching_tolerance"] is True
    assert val_report["rules"]["10_hidden_state_isolation"] is True
    assert val_report["rules"]["15_zero_future_leakage"] is True
