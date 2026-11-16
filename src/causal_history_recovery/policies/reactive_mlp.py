"""Reactive Memoryless MLP Policy.

Implements a deterministic feedforward multilayer perceptron mapping instantaneous
observation o(t) ∈ ℝ²⁰ directly to action a(t) ∈ ℝ³, with zero historical memory.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
import numpy as np
import torch
import torch.nn as nn

from causal_history_recovery.policies.base_policy import BasePolicy


class _MLPNetwork(nn.Module):
    """Internal PyTorch feedforward module."""

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        hidden_dims: List[int],
        action_limit: float = 0.02,
        activation: str = "relu",
    ):
        super().__init__()
        act_cls = nn.ReLU if activation.lower() == "relu" else nn.Tanh

        layers = []
        prev_dim = obs_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(act_cls())
            prev_dim = h_dim

        layers.append(nn.Linear(prev_dim, action_dim))
        self.network = nn.Sequential(*layers)
        self.action_limit = action_limit

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        raw_out = self.network(obs)
        return torch.tanh(raw_out) * self.action_limit


class ReactiveMLPPolicy(BasePolicy):
    """Reactive MLP Policy operating strictly without observation or action history."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.hidden_dims = list(config.get("hidden_dims", [128, 128]))
        self.activation = str(config.get("activation", "relu"))

        self.model = _MLPNetwork(
            obs_dim=self.obs_dim,
            action_dim=self.action_dim,
            hidden_dims=self.hidden_dims,
            action_limit=self.action_limit,
            activation=self.activation,
        ).to(self.device)

        self.model.eval()

    def act(
        self,
        observation: np.ndarray,
        *,
        deterministic: bool = True,
    ) -> np.ndarray:
        """Compute action from instantaneous observation."""
        with torch.no_grad():
            obs_t = torch.as_tensor(observation, dtype=torch.float32, device=self.device)
            if obs_t.ndim == 1:
                obs_t = obs_t.unsqueeze(0)
            action_t = self.model(obs_t)
            action = action_t.squeeze(0).cpu().numpy()
            return np.clip(action, -self.action_limit, self.action_limit)

    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """No-op for memoryless policy."""
        pass

    def get_hidden_state(self) -> Optional[Any]:
        """MLP is stateless; returns None."""
        return None

    def set_hidden_state(self, hidden_state: Optional[Any]) -> None:
        """No-op for stateless policy."""
        pass

    def reset_hidden_state(self) -> None:
        """No-op for stateless policy."""
        pass

    def save(self, path: str) -> None:
        """Save model checkpoint and configuration metadata."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        checkpoint = {
            "policy_type": "reactive_mlp",
            "state_dict": self.model.state_dict(),
            "config": self.config,
        }
        torch.save(checkpoint, path)

    def load(self, path: str) -> None:
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint["state_dict"])
        self.model.eval()

