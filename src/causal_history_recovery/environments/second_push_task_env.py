"""Second Push Task Environment (SecondPushTaskEnv).

A tabletop manipulation task featuring:
- Cylindrical puck object (mass = 0.15 kg, radius = 0.035 m, half-height = 0.020 m)
- Lower surface Coulomb friction (mu = 0.35)
- Continuous curved contact manifold (cylinder-on-cylinder)
- Diagonal push direction toward an offset goal [0.20, 0.08, 0.020]
- Bitwise deterministic state snapshotting and restoration
- Strict binary task success with dwell criteria.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import mujoco

from causal_history_recovery.environments.base_env import BaseRoboticEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.environments.contact_extractor import ContactExtractor, ContactPoint


class SecondPushTaskEnv(BaseRoboticEnv):
    """Second manipulation task with distinct geometry, mass, friction, and goal angle."""

    metadata = {"render_modes": ["rgb_array"]}

    def __init__(
        self,
        xml_path: Optional[str] = None,
        max_horizon: int = 150,
        target_radius: float = 0.065,
        target_pos: Optional[np.ndarray] = None,
        min_dwell_steps: int = 5,
        max_yaw_tolerance_rad: float = 0.50,  # ~28.6 degrees
    ):
        super().__init__()

        if xml_path is None:
            xml_path = os.path.join(os.path.dirname(__file__), "assets", "second_push_target.xml")
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"Model XML not found at {xml_path}")

        self.xml_path = xml_path
        self.model: mujoco.MjModel = mujoco.MjModel.from_xml_path(xml_path)
        self.data: mujoco.MjData = mujoco.MjData(self.model)

        self._max_horizon = max_horizon
        self._target_radius = target_radius
        self._target_pos = np.array(target_pos or [0.20, 0.08, 0.020], dtype=np.float64)
        self._min_dwell_steps = min_dwell_steps
        self._max_yaw_tolerance = max_yaw_tolerance_rad

        self._step_count = 0
        self._dwell_count = 0
        self._current_seed: Optional[int] = None
        self._np_random = np.random.RandomState()

        self.contact_extractor = ContactExtractor(self.model)

        # Action space: Cartesian delta [dx, dy, dz] bounded in [-0.02, 0.02]
        self.action_space = spaces.Box(
            low=-0.02, high=0.02, shape=(3,), dtype=np.float32
        )

        # Observation space: 20-dim continuous state representation
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(20,), dtype=np.float32
        )

        # Lookups
        self.pusher_geom_id = self.model.geom("pusher_geom").id
        self.object_geom_id = self.model.geom("object_geom").id
        self.table_geom_id = self.model.geom("table").id
        self.object_body_id = self.model.body("target_object").id

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
        if seed is not None:
            self._current_seed = seed
            self._np_random = np.random.RandomState(seed)

        self._step_count = 0
        self._dwell_count = 0

        mujoco.mj_resetData(self.model, self.data)

        # Initial object pose: cylinder radius 0.035, half-height 0.020, resting at z=0.020
        obj_x_jitter = self._np_random.uniform(-0.01, 0.01) if seed is not None else 0.0
        obj_y_jitter = self._np_random.uniform(-0.01, 0.01) if seed is not None else 0.0

        # Pusher initial pose behind puck
        self.data.qpos[0] = -0.08
        self.data.qpos[1] = 0.0
        self.data.qpos[2] = 0.0

        self.data.qpos[3] = obj_x_jitter
        self.data.qpos[4] = obj_y_jitter
        self.data.qpos[5] = 0.020
        self.data.qpos[6:10] = [1.0, 0.0, 0.0, 0.0]

        self.data.qvel[:] = 0.0
        self.data.ctrl[0] = self.data.qpos[0]
        self.data.ctrl[1] = self.data.qpos[1]
        self.data.ctrl[2] = self.data.qpos[2]

        mujoco.mj_forward(self.model, self.data)

        obs = self._get_observation()
        info = {
            "step_count": self._step_count,
            "remaining_horizon": self.remaining_horizon,
            "is_success": False,
            "dwell_count": 0,
            "object_pos": self.get_object_position(),
            "object_yaw_rad": self.get_object_yaw(),
            "task_goal": self.get_task_goal(),
        }
        return obs, info

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        self._step_count += 1
        action = np.clip(action, self.action_space.low, self.action_space.high)

        self.data.ctrl[0] = float(np.clip(self.data.ctrl[0] + action[0], -0.45, 0.45))
        self.data.ctrl[1] = float(np.clip(self.data.ctrl[1] + action[1], -0.45, 0.45))
        self.data.ctrl[2] = float(np.clip(self.data.ctrl[2] + action[2], -0.01, 0.15))

        mujoco.mj_step(self.model, self.data)
        mujoco.mj_forward(self.model, self.data)

        obs = self._get_observation()
        dist_to_goal = float(np.linalg.norm(self.get_object_position()[:2] - self._target_pos[:2]))
        yaw_rad = self.get_object_yaw()

        in_target = dist_to_goal <= self._target_radius
        yaw_aligned = abs(yaw_rad) <= self._max_yaw_tolerance

        if in_target and yaw_aligned:
            self._dwell_count += 1
        else:
            self._dwell_count = 0

        is_success = bool(self._dwell_count >= self._min_dwell_steps)

        obj_pos = self.get_object_position()
        fallen = bool(obj_pos[2] < 0.008)
        out_of_bounds = bool(abs(obj_pos[0]) > 0.45 or abs(obj_pos[1]) > 0.45)
        terminated = bool(fallen or out_of_bounds)
        truncated = bool(self._step_count >= self._max_horizon)

        reward = -dist_to_goal + (10.0 if is_success else 0.0)

        info = {
            "step_count": self._step_count,
            "remaining_horizon": self.remaining_horizon,
            "is_success": is_success,
            "dwell_count": self._dwell_count,
            "dist_to_goal": dist_to_goal,
            "object_yaw_rad": yaw_rad,
            "object_pos": obj_pos,
            "fallen": fallen,
            "out_of_bounds": out_of_bounds,
            "has_pusher_contact": self._has_pusher_contact(),
        }
        return obs, float(reward), terminated, truncated, info

    def get_state_snapshot(self) -> StateSnapshot:
        obj_pos = self.get_object_position()
        ee_pos = self.get_end_effector_position()
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
            object_rot=self.data.qpos[6:10].copy(),
            end_effector_pos=ee_pos,
            active_contacts_count=len(contacts),
            metadata={
                "env_id": "second_push_task_env",
                "object_geometry": "cylinder",
                "object_mass": 0.15,
                "surface_friction": 0.35,
                "current_seed": self._current_seed,
                "dwell_count": self._dwell_count,
                "timestep": float(self.model.opt.timestep),
            },
        )

    def restore_state_snapshot(self, snapshot: StateSnapshot) -> None:
        self.data.qpos[:] = snapshot.qpos.copy()
        self.data.qvel[:] = snapshot.qvel.copy()
        self.data.time = float(snapshot.time)

        if snapshot.qacc_warmstart is not None:
            self.data.qacc_warmstart[:] = snapshot.qacc_warmstart.copy()
        if snapshot.qfrc_applied is not None:
            self.data.qfrc_applied[:] = snapshot.qfrc_applied.copy()
        if snapshot.xfrc_applied is not None:
            self.data.xfrc_applied[:] = snapshot.xfrc_applied.copy()
        if snapshot.ctrl is not None:
            self.data.ctrl[:] = snapshot.ctrl.copy()

        self._step_count = int(snapshot.step_count)
        self._max_horizon = int(snapshot.max_horizon)
        if snapshot.metadata and "dwell_count" in snapshot.metadata:
            self._dwell_count = int(snapshot.metadata["dwell_count"])
        if snapshot.metadata and "current_seed" in snapshot.metadata:
            self._current_seed = snapshot.metadata["current_seed"]

        if snapshot.task_goal is not None:
            self._target_pos = snapshot.task_goal.copy()

        mujoco.mj_forward(self.model, self.data)

    def inject_matched_state(
        self,
        snapshot: StateSnapshot,
        *,
        preserve_horizon: bool = True,
    ) -> np.ndarray:
        self.restore_state_snapshot(snapshot)
        if not preserve_horizon:
            self._step_count = 0
        mujoco.mj_forward(self.model, self.data)
        return self._get_observation()

    def get_physical_state(self) -> np.ndarray:
        return np.concatenate([self.data.qpos, self.data.qvel]).copy()

    def get_task_goal(self) -> np.ndarray:
        return self._target_pos.copy()

    def set_task_goal(self, goal: np.ndarray) -> None:
        self._target_pos = np.array(goal, dtype=np.float64)

    def get_object_position(self) -> np.ndarray:
        return self.data.qpos[3:6].copy()

    def get_object_velocity(self) -> np.ndarray:
        return self.data.qvel[3:6].copy()

    def get_object_yaw(self) -> float:
        quat = self.data.qpos[6:10]
        w, x, y, z = quat
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        return float(np.arctan2(siny_cosp, cosy_cosp))

    def get_end_effector_position(self) -> np.ndarray:
        return self.data.geom_xpos[self.pusher_geom_id].copy()

    def get_end_effector_velocity(self) -> np.ndarray:
        return self.data.qvel[:3].copy()

    def get_contacts(self) -> List[ContactPoint]:
        return self.contact_extractor.extract_contacts(self.data)

    def get_environment_metadata(self) -> Dict[str, Any]:
        return {
            "env_id": "second_push_task_env",
            "nq": int(self.model.nq),
            "nv": int(self.model.nv),
            "nu": int(self.model.nu),
            "timestep": float(self.model.opt.timestep),
            "max_horizon": self._max_horizon,
            "target_radius": self._target_radius,
            "target_pos": self._target_pos.tolist(),
            "min_dwell_steps": self._min_dwell_steps,
            "max_yaw_tolerance_rad": self._max_yaw_tolerance,
            "object_geometry": "cylinder",
            "object_mass": 0.15,
            "surface_friction": 0.35,
        }

    def _has_pusher_contact(self) -> bool:
        contacts = self.get_contacts()
        for c in contacts:
            if (c.geom1_id == self.pusher_geom_id and c.geom2_id == self.object_geom_id) or \
               (c.geom1_id == self.object_geom_id and c.geom2_id == self.pusher_geom_id):
                return True
        return False

    def _get_observation(self) -> np.ndarray:
        ee_pos = self.get_end_effector_position()
        ee_vel = self.get_end_effector_velocity()
        obj_pos = self.get_object_position()
        yaw = self.get_object_yaw()
        cos_yaw = float(np.cos(yaw))
        sin_yaw = float(np.sin(yaw))
        obj_lin_vel = self.get_object_velocity()
        obj_ang_vel = self.data.qvel[6:9].copy() if len(self.data.qvel) >= 9 else np.zeros(3)
        goal_pos = self.get_task_goal()

        obs = np.concatenate([
            ee_pos,
            ee_vel,
            obj_pos,
            np.array([cos_yaw, sin_yaw], dtype=np.float32),
            obj_lin_vel,
            obj_ang_vel,
            goal_pos,
        ], dtype=np.float32)

        return obs
