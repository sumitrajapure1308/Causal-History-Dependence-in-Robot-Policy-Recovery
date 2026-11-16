"""Recovery-Augmented MLP Policy.

Implements a non-recurrent policy conditioned on an augmented observation token:
- Base observation o_t (20 dimensions)
- Real-time failure detection signal (1 dimension)
- Normalized deviation duration indicator (1 dimension)
- Estimated deviation magnitude (1 dimension)
- Remaining episode horizon (1 dimension)

Total input dimension: 24 dimensions.
Uses NO future observations, actions, rewards, or oracle-privileged ground truths.
"""

from __future__ import annotations

import collections
import os
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn

from causal_history_recovery.policies.base_policy import BasePolicy


class _RecoveryMLPNetwork(nn.Module):
    """Feedforward network with recovery-specific conditioning."""

    def __init__(
        self,
        input_dim: int = 24,
        action_dim: int = 3,
        hidden_dims: Tuple[int, ...] = (128, 128),
        action_limit: float = 0.02,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.action_dim = action_dim
        self.action_limit = action_limit

        layers: List[nn.Module] = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.LayerNorm(h_dim))
            layers.append(nn.ReLU())
            prev_dim = h_dim

        layers.append(nn.Linear(prev_dim, action_dim))
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raw_out = self.network(x)
        return torch.tanh(raw_out) * self.action_limit


class RecoveryAugmentedMLPPolicy(BasePolicy):
    """Non-recurrent policy augmented with causal failure and horizon state indicators."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.action_limit = float(config.get("action_limit", 0.02))
        hidden_dims = tuple(config.get("hidden_dims", [128, 128]))

        # Base obs (20) + failure_detected (1) + deviation_time (1) + deviation_mag (1) + horizon (1) = 24
        self.augmented_dim = self.obs_dim + 4

        self.model = _RecoveryMLPNetwork(
            input_dim=self.augmented_dim,
            action_dim=self.action_dim,
            hidden_dims=hidden_dims,
            action_limit=self.action_limit,
        ).to(self.device)

        # Internal online detector state
        self.step_count = 0
        self.deviation_detected = False
        self.deviation_step = 0

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        self.step_count = 0
        self.deviation_detected = False
        self.deviation_step = 0

    def compute_augmented_features(
        self,
        observation: np.ndarray,
        remaining_horizon: Optional[float] = None,
    ) -> np.ndarray:
        """Compute online causal deviation estimates from current observation."""
        self.step_count += 1
        # Extract orientation components: cos(yaw), sin(yaw) at indices 6, 7 in obj orientation
        cos_yaw = observation[9]
        sin_yaw = observation[10]
        yaw = float(np.arctan2(sin_yaw, cos_yaw))
        obj_y = float(observation[7])

        # Online detection rule: yaw > 15 deg (0.26 rad) or drift > 2.5 cm
        yaw_dev = abs(yaw)
        drift_dev = abs(obj_y)

        if not self.deviation_detected and (yaw_dev > 0.26 or drift_dev > 0.025):
            self.deviation_detected = True
            self.deviation_step = self.step_count

        failure_flag = 1.0 if self.deviation_detected else 0.0
        dev_time = (self.step_count - self.deviation_step) / 100.0 if self.deviation_detected else 0.0
        dev_mag = yaw_dev if self.deviation_detected else 0.0
        rem_horiz = remaining_horizon if remaining_horizon is not None else max(0.0, (150.0 - self.step_count) / 150.0)

        aug_vector = np.concatenate([
            observation,
            np.array([failure_flag, dev_time, dev_mag, rem_horiz], dtype=np.float32),
        ], dtype=np.float32)

        return aug_vector

    def act(
        self,
        observation: np.ndarray,
        *,
        deterministic: bool = True,
        remaining_horizon: Optional[float] = None,
    ) -> np.ndarray:
        aug_obs = self.compute_augmented_features(observation, remaining_horizon)

        with torch.no_grad():
            x = torch.as_tensor(aug_obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            action = self.model(x).squeeze(0).cpu().numpy()

        return np.clip(action, -self.action_limit, self.action_limit)

    def get_hidden_state(self) -> Optional[Any]:
        return None

    def set_hidden_state(self, hidden_state: Optional[Any]) -> None:
        pass

    def reset_hidden_state(self) -> None:
        pass

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        torch.save({
            "policy_type": "recovery_augmented_mlp",
            "state_dict": self.model.state_dict(),
            "config": self.config,
        }, path)

    def load(self, path: str) -> None:
        data = torch.load(path, map_location=self.device)
        self.model.load_state_dict(data["state_dict"])
        self.model.eval()
