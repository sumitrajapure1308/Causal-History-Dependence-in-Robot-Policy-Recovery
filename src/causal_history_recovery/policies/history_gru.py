"""History-Aware GRU Recurrent Policy.

Implements a recurrent GRU network conditioned on current observation o(t),
past observation-action history sequence (o_{t-k:t}, a_{t-k:t-1}), and internal hidden state h(t).
Supports selective counterfactual ablation of observation history (B2), action history (B1),
and recurrent memory reset (B3 / B4).
"""

from __future__ import annotations

import collections
import os
from typing import Any, Deque, Dict, List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn

from causal_history_recovery.policies.base_policy import BasePolicy


class _GRUNetwork(nn.Module):
    """PyTorch Recurrent GRU Module for sequential decision-making."""

    def __init__(
        self,
        input_dim: int,
        action_dim: int,
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
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim),
        )

    def forward(
        self,
        x_seq: torch.Tensor,
        h_0: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass over sequence of tokens (B, T, input_dim)."""
        gru_out, h_n = self.gru(x_seq, h_0)
        raw_actions = self.fc_head(gru_out)
        actions = torch.tanh(raw_actions) * self.action_limit
        return actions, h_n


class HistoryGRUPolicy(BasePolicy):
    """History-Aware Policy with configurable sliding window and recurrent memory."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.history_window = int(config.get("history_window", 10))
        self.hidden_dim = int(config.get("hidden_dim", 128))
        self.num_layers = int(config.get("num_layers", 1))

        # Input dimension: obs_dim (20) + prev_action_dim (3) = 23
        self.input_dim = self.obs_dim + self.action_dim

        self.model = _GRUNetwork(
            input_dim=self.input_dim,
            action_dim=self.action_dim,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers,
            action_limit=self.action_limit,
        ).to(self.device)

        self.model.eval()

        # Rolling historical buffers for evaluation rollouts
        self.obs_buffer: Deque[np.ndarray] = collections.deque(maxlen=self.history_window)
        self.action_buffer: Deque[np.ndarray] = collections.deque(maxlen=self.history_window)
        self.hidden_state: Optional[torch.Tensor] = None

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """Reset internal history buffers and recurrent hidden state."""
        self.obs_buffer.clear()
        self.action_buffer.clear()
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

    def act(
        self,
        observation: np.ndarray,
        *,
        deterministic: bool = True,
    ) -> np.ndarray:
        """Step the policy forward by one timestep with current observation."""
        if len(self.obs_buffer) == 0:
            self.reset(observation)

        # Update observation buffer
        self.obs_buffer.append(observation.copy())

        # Construct single-step input token: [o_t, a_{t-1}]
        prev_action = self.action_buffer[-1]
        token = np.concatenate([observation, prev_action], dtype=np.float32)

        with torch.no_grad():
            token_t = torch.as_tensor(token, dtype=torch.float32, device=self.device).view(1, 1, -1)
            actions_t, self.hidden_state = self.model(token_t, self.hidden_state)
            action = actions_t.squeeze(0).squeeze(0).cpu().numpy()

        action = np.clip(action, -self.action_limit, self.action_limit)
        self.action_buffer.append(action.copy())
        return action

    def get_hidden_state(self) -> Optional[torch.Tensor]:
        """Return detached copy of current recurrent hidden state."""
        if self.hidden_state is None:
            return None
        return self.hidden_state.detach().clone()

    def set_hidden_state(self, hidden_state: Optional[torch.Tensor]) -> None:
        """Set the internal recurrent hidden state."""
        if hidden_state is None:
            self.reset_hidden_state()
        else:
            self.hidden_state = hidden_state.to(self.device).detach().clone()

    def reset_hidden_state(self) -> None:
        """Zero out the recurrent hidden state (Condition B3 intervention)."""
        self.hidden_state = torch.zeros(
            (self.num_layers, 1, self.hidden_dim),
            dtype=torch.float32,
            device=self.device,
        )

    def ablate_history(
        self,
        current_obs: np.ndarray,
        *,
        ablate_obs: bool = False,
        ablate_act: bool = False,
    ) -> None:
        """Ablate observation and/or action history for counterfactual conditions (B1, B2, B4)."""
        if ablate_obs:
            # Overwrite past observations with current observation
            self.obs_buffer.clear()
            for _ in range(self.history_window):
                self.obs_buffer.append(current_obs.copy())

        if ablate_act:
            # Overwrite past actions with zeros
            self.action_buffer.clear()
            zero_act = np.zeros(self.action_dim, dtype=np.float32)
            for _ in range(self.history_window):
                self.action_buffer.append(zero_act.copy())

    def has_recurrent_memory(self) -> bool:
        """Return True indicating recurrent memory architecture."""
        return True

    def get_memory_state(self) -> Dict[str, Any]:
        """Capture complete serializable snapshot of internal memory state."""
        return {
            "type": "history_gru",
            "hidden_state": self.hidden_state.detach().clone() if self.hidden_state is not None else None,
            "obs_buffer": [o.copy() for o in self.obs_buffer],
            "action_buffer": [a.copy() for a in self.action_buffer],
            "history_window": self.history_window,
        }

    def set_memory_state(self, memory_state: Dict[str, Any]) -> None:
        """Restore internal memory state bitwise from snapshot."""
        if memory_state.get("hidden_state") is not None:
            self.hidden_state = memory_state["hidden_state"].to(self.device).detach().clone()
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

    def reset_memory(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """Explicitly reset history buffers and zero recurrent hidden state."""
        self.reset(initial_obs)

    def get_history_summary(self) -> Dict[str, Any]:
        """Return diagnostic metrics on current history state."""
        return {
            "history_window": self.history_window,
            "obs_buffered": len(self.obs_buffer),
            "actions_buffered": len(self.action_buffer),
            "hidden_norm": float(torch.norm(self.hidden_state).item()) if self.hidden_state is not None else 0.0,
        }

    def save(self, path: str) -> None:
        """Save model checkpoint and configuration metadata."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        checkpoint = {
            "policy_type": "history_gru",
            "state_dict": self.model.state_dict(),
            "config": self.config,
        }
        torch.save(checkpoint, path)

    def load(self, path: str) -> None:
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint["state_dict"])
        self.model.eval()

