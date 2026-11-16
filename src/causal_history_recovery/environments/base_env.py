"""Base Robotic Environment Interface for Causal-History-Recovery.

Defines the core abstract class that all benchmark and candidate environments must
implement to support deterministic snapshotting, state matching, and causal replay.
"""

from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional, Tuple
import gymnasium as gym
import numpy as np

from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.environments.contact_extractor import ContactPoint


class BaseRoboticEnv(gym.Env, abc.ABC):
    """Abstract base class for environments supporting causal-history evaluations."""

    @abc.abstractmethod
    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment with explicit seed control."""
        pass

    @abc.abstractmethod
    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Execute one simulation step and return (obs, reward, terminated, truncated, info)."""
        pass

    @abc.abstractmethod
    def get_state_snapshot(self) -> StateSnapshot:
        """Capture an exact, complete Markovian snapshot of the current state."""
        pass

    @abc.abstractmethod
    def restore_state_snapshot(self, snapshot: StateSnapshot) -> None:
        """Restore environment to an exact previous snapshot with bitwise fidelity."""
        pass

    @abc.abstractmethod
    def inject_matched_state(
        self,
        snapshot: StateSnapshot,
        *,
        preserve_horizon: bool = True,
    ) -> np.ndarray:
        """Inject a physically matched state without preceding action history.
        
        Returns the new instantaneous observation after injection.
        """
        pass

    @abc.abstractmethod
    def get_physical_state(self) -> np.ndarray:
        """Return the unnormalized low-dimensional physical state vector."""
        pass

    @abc.abstractmethod
    def get_task_goal(self) -> np.ndarray:
        """Return the target goal coordinates."""
        pass

    @abc.abstractmethod
    def get_contacts(self) -> List[ContactPoint]:
        """Return structured list of active contact points."""
        pass

    @property
    @abc.abstractmethod
    def step_count(self) -> int:
        """Current elapsed steps in this episode."""
        pass

    @property
    @abc.abstractmethod
    def remaining_horizon(self) -> int:
        """Remaining step budget in this episode."""
        pass

    @property
    @abc.abstractmethod
    def max_horizon(self) -> int:
        """Maximum total steps allowed in an episode."""
        pass

    @abc.abstractmethod
    def get_environment_metadata(self) -> Dict[str, Any]:
        """Return environment parameters, physics constants, and kinematics."""
        pass

