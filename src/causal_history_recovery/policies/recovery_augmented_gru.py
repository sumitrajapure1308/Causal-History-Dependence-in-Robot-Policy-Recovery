"""Recovery-Augmented GRU Recurrent Policy.

Implements a recurrent GRU policy conditioned on:
- Augmented observation (base observation 20 + failure detection 1 + dev time 1 + dev mag 1 + horizon 1 = 24 dims)
- Previous action (3 dims)
- Contact state indicator (1 dim)
- Internal recurrent hidden state h(t) (128 dims)

Total input token dimension: 24 + 3 + 1 = 28 dims.
Supports counterfactual history ablations:
- B0: Full preserved history (intact hidden state and action/obs buffers)
- B1: Action history zero-masked
- B2: Observation history window padded with current state
- B3: Hidden state reset to zero
- B4: All history removed (isolated matched-state injection)
"""

from __future__ import annotations

import collections
import os
from typing import Any, Deque, Dict, List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn

from causal_history_recovery.policies.base_policy import BasePolicy


class _RecoveryGRUNetwork(nn.Module):
    """PyTorch Recurrent GRU Module for sequential recovery decision-making."""

    def __init__(
        self,
        input_dim: int = 28,
        action_dim: int = 3,
        hidden_dim: int = 128,
        num_layers: int = 1,
        action_limit: float = 0.02,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.action_limit = action_limit

        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.fc_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.LayerNorm(hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim),
        )

    def forward(
        self,
        x_seq: torch.Tensor,
        h_0: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        gru_out, h_n = self.gru(x_seq, h_0)
        raw_actions = self.fc_head(gru_out)
        actions = torch.tanh(raw_actions) * self.action_limit
        return actions, h_n


class RecoveryAugmentedGRUPolicy(BasePolicy):
    """Recurrent policy augmented with causal failure features and counterfactual ablation support."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.history_window = int(config.get("history_window", 10))
        self.hidden_dim = int(config.get("hidden_dim", 128))
        self.num_layers = int(config.get("num_layers", 1))
        self.action_limit = float(config.get("action_limit", 0.02))

        # Augmented obs (24) + prev_action (3) + contact (1) = 28
        self.input_dim = 24 + self.action_dim + 1

        self.model = _RecoveryGRUNetwork(
            input_dim=self.input_dim,
            action_dim=self.action_dim,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers,
            action_limit=self.action_limit,
        ).to(self.device)

        # Buffers
        self.obs_buffer: Deque[np.ndarray] = collections.deque(maxlen=self.history_window)
        self.action_buffer: Deque[np.ndarray] = collections.deque(maxlen=self.history_window)
        self.contact_buffer: Deque[float] = collections.deque(maxlen=self.history_window)
        self.hidden_state: Optional[torch.Tensor] = None

        # Online detection state
        self.step_count = 0
        self.deviation_detected = False
        self.deviation_step = 0

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        self.step_count = 0
        self.deviation_detected = False
        self.deviation_step = 0
        self.obs_buffer.clear()
        self.action_buffer.clear()
        self.contact_buffer.clear()

        self.hidden_state = torch.zeros(
            (self.num_layers, 1, self.hidden_dim),
            dtype=torch.float32,
            device=self.device,
        )

        init_obs = initial_obs if initial_obs is not None else np.zeros(self.obs_dim, dtype=np.float32)
        zero_action = np.zeros(self.action_dim, dtype=np.float32)

        for _ in range(self.history_window):
            self.obs_buffer.append(init_obs.copy())
            self.action_buffer.append(zero_action.copy())
            self.contact_buffer.append(0.0)

    def reset_hidden_state(self) -> None:
        self.hidden_state = torch.zeros(
            (self.num_layers, 1, self.hidden_dim),
            dtype=torch.float32,
            device=self.device,
        )

    def compute_augmented_features(
        self,
        observation: np.ndarray,
        remaining_horizon: Optional[float] = None,
    ) -> np.ndarray:
        self.step_count += 1
        cos_yaw = observation[9]
        sin_yaw = observation[10]
        yaw = float(np.arctan2(sin_yaw, cos_yaw))
        obj_y = float(observation[7])

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
        contact_present: float = 0.0,
    ) -> np.ndarray:
        if len(self.obs_buffer) == 0:
            self.reset(observation)

        aug_obs = self.compute_augmented_features(observation, remaining_horizon)
        self.obs_buffer.append(aug_obs.copy())
        self.contact_buffer.append(float(contact_present))

        prev_action = self.action_buffer[-1]
        prev_contact = np.array([self.contact_buffer[-1]], dtype=np.float32)

        token = np.concatenate([aug_obs, prev_action, prev_contact], dtype=np.float32)

        with torch.no_grad():
            token_t = torch.as_tensor(token, dtype=torch.float32, device=self.device).view(1, 1, -1)
            actions_t, self.hidden_state = self.model(token_t, self.hidden_state)
            action = actions_t.squeeze(0).squeeze(0).cpu().numpy()

        action = np.clip(action, -self.action_limit, self.action_limit)
        self.action_buffer.append(action.copy())
        return action

    def get_hidden_state(self) -> Optional[torch.Tensor]:
        if self.hidden_state is None:
            return None
        return self.hidden_state.detach().clone()

    def set_hidden_state(self, hidden_state: Optional[torch.Tensor]) -> None:
        if hidden_state is None:
            self.reset_hidden_state()
        else:
            self.hidden_state = hidden_state.detach().clone().to(self.device)

    def has_recurrent_memory(self) -> bool:
        """Return True indicating recurrent memory architecture."""
        return True

    def get_memory_state(self) -> Dict[str, Any]:
        """Capture complete serializable snapshot of internal memory state."""
        return {
            "type": "recovery_augmented_gru",
            "hidden_state": self.hidden_state.detach().clone() if self.hidden_state is not None else None,
            "obs_buffer": [o.copy() for o in self.obs_buffer],
            "action_buffer": [a.copy() for a in self.action_buffer],
            "contact_buffer": list(self.contact_buffer),
            "step_count": int(self.step_count),
            "deviation_detected": bool(self.deviation_detected),
            "deviation_step": int(self.deviation_step),
            "history_window": int(self.history_window),
        }

    def set_memory_state(self, memory_state: Dict[str, Any]) -> None:
        """Restore internal memory state bitwise from snapshot."""
        if memory_state.get("hidden_state") is not None:
            self.hidden_state = memory_state["hidden_state"].detach().clone().to(self.device)
        else:
            self.reset_hidden_state()

        if "obs_buffer" in memory_state:
            self.obs_buffer.clear()
            for o in memory_state["obs_buffer"]:
                self.obs_buffer.append(np.array(o, dtype=np.float32).copy())

        if "action_buffer" in memory_state:
            self.action_buffer.clear()
            for a in memory_state["action_buffer"]:
                self.action_buffer.append(np.array(a, dtype=np.float32).copy())

        if "contact_buffer" in memory_state:
            self.contact_buffer.clear()
            for c in memory_state["contact_buffer"]:
                self.contact_buffer.append(float(c))

        if "step_count" in memory_state:
            self.step_count = int(memory_state["step_count"])
        if "deviation_detected" in memory_state:
            self.deviation_detected = bool(memory_state["deviation_detected"])
        if "deviation_step" in memory_state:
            self.deviation_step = int(memory_state["deviation_step"])

    def reset_memory(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """Explicitly reset history buffers, online detection state, and hidden state."""
        self.reset(initial_obs)

    def apply_counterfactual_condition(
        self,
        condition_id: str,
        current_observation: np.ndarray,
    ) -> None:
        """Apply counterfactual history ablation rule before recovery begins."""
        aug_curr = self.compute_augmented_features(current_observation)

        if condition_id == "B0":
            pass
        elif condition_id == "B1":
            zero_act = np.zeros(self.action_dim, dtype=np.float32)
            for i in range(len(self.action_buffer)):
                self.action_buffer[i] = zero_act.copy()
        elif condition_id == "B2":
            for i in range(len(self.obs_buffer)):
                self.obs_buffer[i] = aug_curr.copy()
        elif condition_id == "B3":
            self.reset_hidden_state()
        elif condition_id == "B4":
            self.reset_hidden_state()
            zero_act = np.zeros(self.action_dim, dtype=np.float32)
            for i in range(len(self.action_buffer)):
                self.action_buffer[i] = zero_act.copy()
            for i in range(len(self.obs_buffer)):
                self.obs_buffer[i] = aug_curr.copy()
            for i in range(len(self.contact_buffer)):
                self.contact_buffer[i] = 0.0

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        torch.save({
            "policy_type": "recovery_augmented_gru",
            "state_dict": self.model.state_dict(),
            "config": self.config,
        }, path)

    def load(self, path: str) -> None:
        data = torch.load(path, map_location=self.device)
        self.model.load_state_dict(data["state_dict"])
        self.model.eval()
