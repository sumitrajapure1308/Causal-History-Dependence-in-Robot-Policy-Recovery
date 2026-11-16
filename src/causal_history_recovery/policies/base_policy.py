"""Base Policy Interface for Robot Recovery Evaluation.

Defines the abstract interface that all recovery policies (MLP, GRU, Oracle) must implement.
Guarantees consistent action spaces, observation preprocessing, deterministic evaluation,
checkpoint serialization, and explicit history/hidden-state intervention hooks.
"""

from __future__ import annotations

import abc
from typing import Any, Dict, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn


class BasePolicy(abc.ABC):
    """Abstract base class for all learned and scripted policies."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device(config.get("device", "cpu"))
        self.action_dim = int(config.get("action_dim", 3))
        self.obs_dim = int(config.get("obs_dim", 20))
        self.action_limit = float(config.get("action_limit", 0.02))

    @abc.abstractmethod
    def act(
        self,
        observation: np.ndarray,
        *,
        deterministic: bool = True,
    ) -> np.ndarray:
        """Compute an action given current observation.
        
        Args:
            observation: Current environment observation (obs_dim,).
            deterministic: Whether to evaluate deterministically (argmax/mean).
            
        Returns:
            action: Continuous action vector (action_dim,) clipped to [-action_limit, action_limit].
        """
        pass

    @abc.abstractmethod
    def reset(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """Reset internal history buffers and recurrent hidden states for a new episode."""
        pass

    @abc.abstractmethod
    def get_hidden_state(self) -> Optional[Any]:
        """Return the current recurrent hidden state (or None for memoryless policies)."""
        pass

    @abc.abstractmethod
    def set_hidden_state(self, hidden_state: Optional[Any]) -> None:
        """Set the recurrent hidden state (used for condition B0/B3 interventions)."""
        pass

    @abc.abstractmethod
    def reset_hidden_state(self) -> None:
        """Zero out internal recurrent memory while preserving observation/action history."""
        pass

    def get_memory_state(self) -> Dict[str, Any]:
        """Return full serializable snapshot of policy internal memory state."""
        return {"hidden_state": None, "type": "memoryless"}

    def set_memory_state(self, memory_state: Dict[str, Any]) -> None:
        """Restore full policy memory state from snapshot."""
        pass

    def reset_memory(self, initial_obs: Optional[np.ndarray] = None) -> None:
        """Explicitly reset all internal memory buffers and recurrent hidden states."""
        self.reset(initial_obs)

    def has_recurrent_memory(self) -> bool:
        """Return True if policy possesses recurrent hidden memory, False otherwise."""
        return False

    @abc.abstractmethod
    def save(self, path: str) -> None:
        """Save model weights, configuration, and architecture metadata."""
        pass

    @abc.abstractmethod
    def load(self, path: str) -> None:
        """Load model weights and verify configuration integrity."""
        pass

    def get_config(self) -> Dict[str, Any]:
        """Return policy hyperparameters and architecture configuration."""
        return self.config.copy()

