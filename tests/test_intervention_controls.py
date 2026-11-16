"""Intervention Control Tests: Positive and Negative Instrument Controls.

Implements:
1. SyntheticHistoryDependentToyPolicy:
   - Instrument positive control fixture.
   - Computes actions explicitly conditioned on the difference between past actions and observations.
   - Demonstrably changes its output when history is ablated or altered.
   - LABEL: "Test fixture — not a robotics baseline or scientific result."

2. CurrentObservationOnlyPolicy:
   - Instrument negative control fixture.
   - Computes actions strictly as a static function of instantaneous observation o_t.
   - Demonstrably produces ZERO output difference regardless of history intervention.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional
import numpy as np
import pytest
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.policies.base_policy import BasePolicy


class SyntheticHistoryDependentToyPolicy(BasePolicy):
    """Instrument Positive Control Fixture.
    
    LABEL: Test fixture — not a robotics baseline or scientific result.
    
    Explicitly adds the average of the last 5 executed actions to the output action.
    When history is reset (B4) or action-masked (B1), the output changes demonstrably.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.action_history = []
        self.history_window = 5

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        self.action_history = [np.zeros(self.action_dim, dtype=np.float32) for _ in range(self.history_window)]

    def reset_hidden_state(self) -> None:
        self.action_history = [np.zeros(self.action_dim, dtype=np.float32) for _ in range(self.history_window)]

    def get_hidden_state(self) -> Optional[Any]:
        return None

    def set_hidden_state(self, hidden_state: Optional[Any]) -> None:
        pass

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass

    def act(self, observation: np.ndarray, *, deterministic: bool = True, **kwargs: Any) -> np.ndarray:
        # Base instantaneous action: proportional to first 3 obs dims
        base_act = observation[: self.action_dim] * 0.1
        # Historical modulation: 0.5 * mean of past actions
        hist_term = 0.5 * np.mean(self.action_history[-self.history_window :], axis=0)
        action = base_act + hist_term
        self.action_history.append(action.copy())
        return np.clip(action, -self.action_limit, self.action_limit)


class CurrentObservationOnlyPolicy(BasePolicy):
    """Instrument Negative Control Fixture.
    
    LABEL: Test fixture — strictly current-observation-only negative control.
    
    Computes output action exclusively as a stateless deterministic function of o_t.
    Output is mathematically guaranteed to be invariant to any history intervention.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        pass

    def reset_hidden_state(self) -> None:
        pass

    def get_hidden_state(self) -> Optional[Any]:
        return None

    def set_hidden_state(self, hidden_state: Optional[Any]) -> None:
        pass

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass

    def act(self, observation: np.ndarray, *, deterministic: bool = True, **kwargs: Any) -> np.ndarray:
        # Purely stateless linear projection
        return np.clip(observation[: self.action_dim] * 0.05, -self.action_limit, self.action_limit)


def test_positive_control_history_sensitivity():
    """Verify that the synthetic positive control policy demonstrably reacts to history changes."""
    config = {"obs_dim": 20, "action_dim": 3, "action_limit": 0.02}
    policy = SyntheticHistoryDependentToyPolicy(config)
    obs = np.ones(20, dtype=np.float32) * 0.02

    # Run history prefix
    policy.reset(obs)
    for _ in range(10):
        policy.act(obs)

    # Condition B0 (preserved history)
    act_b0 = policy.act(obs)

    # Condition B4 (history reset)
    policy.reset_hidden_state()
    act_b4 = policy.act(obs)

    diff = np.linalg.norm(act_b0 - act_b4)
    assert diff > 0.001, f"Positive control failed to detect history intervention (diff={diff})"


def test_negative_control_history_invariance():
    """Verify that the negative control policy produces bitwise identical actions under any history."""
    config = {"obs_dim": 20, "action_dim": 3, "action_limit": 0.02}
    policy = CurrentObservationOnlyPolicy(config)
    obs = np.ones(20, dtype=np.float32) * 0.35

    # Run arbitrary sequence
    policy.reset(obs)
    for _ in range(15):
        policy.act(obs)

    act_b0 = policy.act(obs)
    policy.reset_hidden_state()
    act_b4 = policy.act(obs)

    # Mathematically exact equality
    assert np.array_equal(act_b0, act_b4), "Negative control unexpectedly varied under history intervention"
