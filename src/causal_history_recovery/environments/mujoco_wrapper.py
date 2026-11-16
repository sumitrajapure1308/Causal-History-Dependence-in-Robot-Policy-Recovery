"""MuJoCo Environment Wrapper for Causal-History-Recovery.

Wraps Gymnasium MuJoCo environments (including Pusher-v5) and custom MJCF tasks
to provide bitwise-deterministic reset, snapshotting, prefix replay, and state injection.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union
import gymnasium as gym
import numpy as np
import mujoco

from causal_history_recovery.environments.base_env import BaseRoboticEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.environments.contact_extractor import ContactExtractor, ContactPoint


class MuJoCoWrapperEnv(BaseRoboticEnv):
    """Unified wrapper around MuJoCo Gymnasium environments."""

    def __init__(
        self,
        env_or_id: Union[gym.Env, str] = "Pusher-v5",
        max_horizon: int = 100,
        success_distance_threshold: float = 0.05,
    ):
        super().__init__()
        if isinstance(env_or_id, str):
            self.base_env = gym.make(env_or_id)
            self.env_id = env_or_id
        else:
            self.base_env = env_or_id
            self.env_id = getattr(self.base_env.spec, "id", "custom_mujoco_env")

        self._max_horizon = max_horizon
        self._step_count = 0
        self._current_seed: Optional[int] = None
        self._success_threshold = success_distance_threshold

        # Extract underlying MuJoCo model and data handles
        unwrapped = self.base_env.unwrapped
        if not hasattr(unwrapped, "model") or not hasattr(unwrapped, "data"):
            raise ValueError("Underlying environment must expose MuJoCo 'model' and 'data' attributes.")

        self.model: mujoco.MjModel = unwrapped.model
        self.data: mujoco.MjData = unwrapped.data

        self.contact_extractor = ContactExtractor(self.model)

        self.action_space = self.base_env.action_space
        self.observation_space = self.base_env.observation_space

    @property
    def step_count(self) -> int:
        return self._step_count

    @property
    def remaining_horizon(self) -> int:
        return max(0, self._max_horizon - self._step_count)

    @property
    def max_horizon(self) -> int:
        return self._max_horizon

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        self._current_seed = seed
        self._step_count = 0
        obs, info = self.base_env.reset(seed=seed, options=options)

        # Enhance info dictionary with custom tracking
        info["step_count"] = self._step_count
        info["remaining_horizon"] = self.remaining_horizon
        info["is_success"] = self._check_task_success()

        return obs, info

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        self._step_count += 1
        _, reward, terminated, truncated, info = self.base_env.step(action)

        # Forward kinematics synchronization:
        # MuJoCo's mj_step integrates qpos/qvel but does not update body xpos/com until the next forward pass.
        # Calling mj_forward ensures all Cartesian kinematics, body COM, and contact manifolds are
        # bitwise synchronized with the post-step qpos/qvel before observation extraction.
        mujoco.mj_forward(self.model, self.data)
        obs = self._get_current_observation()

        # Explicit horizon truncation
        if self._step_count >= self._max_horizon:
            truncated = True

        is_success = self._check_task_success()
        info["step_count"] = self._step_count
        info["remaining_horizon"] = self.remaining_horizon
        info["is_success"] = is_success

        return obs, float(reward), bool(terminated), bool(truncated), info

    def get_state_snapshot(self) -> StateSnapshot:
        """Capture an exact Markovian state snapshot."""
        # Kinematics extraction
        obj_pos = self._extract_object_position()
        ee_pos = self._extract_end_effector_position()
        contacts = self.contact_extractor.extract_contacts(self.data)

        return StateSnapshot(
            qpos=self.data.qpos.copy(),
            qvel=self.data.qvel.copy(),
            act=self.data.act.copy() if self.data.act is not None and len(self.data.act) > 0 else None,
            qacc_warmstart=self.data.qacc_warmstart.copy(),
            qfrc_applied=self.data.qfrc_applied.copy(),
            xfrc_applied=self.data.xfrc_applied.copy(),
            ctrl=self.data.ctrl.copy(),
            time=float(self.data.time),
            step_count=int(self._step_count),
            remaining_horizon=int(self.remaining_horizon),
            max_horizon=int(self._max_horizon),
            task_goal=self.get_task_goal(),
            object_pos=obj_pos,
            end_effector_pos=ee_pos,
            active_contacts_count=len(contacts),
            metadata={
                "env_id": self.env_id,
                "current_seed": self._current_seed,
                "timestep": float(self.model.opt.timestep),
            },
        )

    def restore_state_snapshot(self, snapshot: StateSnapshot) -> None:
        """Restore exact simulation state with bitwise precision."""
        # 1. Restore generalized state
        self.base_env.unwrapped.set_state(snapshot.qpos, snapshot.qvel)

        # 2. Restore solver & time parameters
        self.data.time = float(snapshot.time)
        if snapshot.qacc_warmstart is not None:
            self.data.qacc_warmstart[:] = snapshot.qacc_warmstart
        if snapshot.qfrc_applied is not None:
            self.data.qfrc_applied[:] = snapshot.qfrc_applied
        if snapshot.xfrc_applied is not None:
            self.data.xfrc_applied[:] = snapshot.xfrc_applied
        if snapshot.ctrl is not None:
            self.data.ctrl[:] = snapshot.ctrl

        # 3. Synchronize step count and horizon
        self._step_count = int(snapshot.step_count)
        self._max_horizon = int(snapshot.max_horizon)

        # 4. Run forward dynamics to repopulate kinematics and contact manifolds
        mujoco.mj_forward(self.model, self.data)

    def inject_matched_state(
        self,
        snapshot: StateSnapshot,
        *,
        preserve_horizon: bool = True,
    ) -> np.ndarray:
        """Inject a physically matched state without preceding action prefix.
        
        Preserves the remaining horizon and goal, while erasing action memory.
        Returns the instantaneous observation post-injection.
        """
        # Restore physical configuration
        self.restore_state_snapshot(snapshot)

        if not preserve_horizon:
            # If horizon is not preserved, reset to full horizon
            self._step_count = 0

        # Run forward pass and get observation
        mujoco.mj_forward(self.model, self.data)
        obs = self._get_current_observation()
        return obs

    def replay_action_prefix(
        self,
        seed: int,
        action_prefix: List[np.ndarray],
    ) -> Tuple[StateSnapshot, List[np.ndarray]]:
        """Replay recorded action prefix deterministically and capture candidate state."""
        self.reset(seed=seed)
        observations = []

        for action in action_prefix:
            obs, _, _, _, _ = self.step(action)
            observations.append(obs)

        snapshot = self.get_state_snapshot()
        return snapshot, observations

    def get_physical_state(self) -> np.ndarray:
        """Return combined (qpos, qvel) as physical state representation."""
        return np.concatenate([self.data.qpos, self.data.qvel]).copy()

    def get_task_goal(self) -> np.ndarray:
        """Extract goal coordinates based on environment layout."""
        if "Pusher" in self.env_id:
            # In Pusher-v5, goal is stored in qpos indices 9, 10
            # [goal_slidey, goal_slidex]
            return np.array([self.data.qpos[10], self.data.qpos[9], 0.0], dtype=np.float64)
        return np.zeros(3, dtype=np.float64)

    def get_contacts(self) -> List[ContactPoint]:
        """Return structured list of active contact points."""
        return self.contact_extractor.extract_contacts(self.data)

    def get_environment_metadata(self) -> Dict[str, Any]:
        """Return environment parameters and configuration."""
        return {
            "env_id": self.env_id,
            "nq": int(self.model.nq),
            "nv": int(self.model.nv),
            "nu": int(self.model.nu),
            "timestep": float(self.model.opt.timestep),
            "max_horizon": self._max_horizon,
            "success_threshold": self._success_threshold,
        }

    def _extract_object_position(self) -> np.ndarray:
        """Extract object Cartesian position."""
        if "Pusher" in self.env_id:
            # obj_slidex is index 8, obj_slidey is index 7
            return np.array([self.data.qpos[8], self.data.qpos[7], 0.0], dtype=np.float64)
        return np.zeros(3, dtype=np.float64)

    def _extract_end_effector_position(self) -> np.ndarray:
        """Extract end-effector Cartesian center."""
        if "Pusher" in self.env_id:
            tip_l = self.data.geom_xpos[self.model.geom("tip_arml").id]
            tip_r = self.data.geom_xpos[self.model.geom("tip_armr").id]
            return (tip_l + tip_r) / 2.0
        return np.zeros(3, dtype=np.float64)

    def _get_current_observation(self) -> np.ndarray:
        """Compute observation vector from current state."""
        # For Pusher-v5, observation is computed by _get_obs() in unwrapped env
        if hasattr(self.base_env.unwrapped, "_get_obs"):
            return self.base_env.unwrapped._get_obs()
        return self.get_physical_state()

    def _check_task_success(self) -> bool:
        """Check whether object has reached the target goal."""
        obj_pos = self._extract_object_position()
        goal_pos = self.get_task_goal()
        dist = float(np.linalg.norm(obj_pos[:2] - goal_pos[:2]))
        return dist <= self._success_threshold
