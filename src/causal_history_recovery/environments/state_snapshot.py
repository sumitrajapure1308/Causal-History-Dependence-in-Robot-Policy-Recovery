"""State Snapshot Module for Causal-History-Recovery.

Provides lossless serialization, deserialization, and distance metrics for
MuJoCo physical simulation states and episode contexts.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, Optional
import numpy as np


@dataclasses.dataclass
class StateSnapshot:
    """Immutable snapshot of the Markovian simulation state and episode metadata."""

    # 1. Generalized coordinates & velocities
    qpos: np.ndarray
    qvel: np.ndarray

    # 2. Solver & actuator state
    act: Optional[np.ndarray] = None
    qacc_warmstart: Optional[np.ndarray] = None
    qfrc_applied: Optional[np.ndarray] = None
    xfrc_applied: Optional[np.ndarray] = None
    ctrl: Optional[np.ndarray] = None

    # 3. Time & horizon tracking
    time: float = 0.0
    step_count: int = 0
    remaining_horizon: int = 0
    max_horizon: int = 100

    # 4. Task goal & kinematics
    task_goal: Optional[np.ndarray] = None
    object_pos: Optional[np.ndarray] = None
    object_rot: Optional[np.ndarray] = None
    end_effector_pos: Optional[np.ndarray] = None

    # 5. Contacts & RNG state
    active_contacts_count: int = 0
    rng_state: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot fields to a serializable dictionary."""
        return {
            "qpos": self.qpos.copy(),
            "qvel": self.qvel.copy(),
            "act": self.act.copy() if self.act is not None else None,
            "qacc_warmstart": self.qacc_warmstart.copy() if self.qacc_warmstart is not None else None,
            "qfrc_applied": self.qfrc_applied.copy() if self.qfrc_applied is not None else None,
            "xfrc_applied": self.xfrc_applied.copy() if self.xfrc_applied is not None else None,
            "ctrl": self.ctrl.copy() if self.ctrl is not None else None,
            "time": float(self.time),
            "step_count": int(self.step_count),
            "remaining_horizon": int(self.remaining_horizon),
            "max_horizon": int(self.max_horizon),
            "task_goal": self.task_goal.copy() if self.task_goal is not None else None,
            "object_pos": self.object_pos.copy() if self.object_pos is not None else None,
            "object_rot": self.object_rot.copy() if self.object_rot is not None else None,
            "end_effector_pos": self.end_effector_pos.copy() if self.end_effector_pos is not None else None,
            "active_contacts_count": int(self.active_contacts_count),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StateSnapshot:
        """Construct StateSnapshot from a dictionary."""
        return cls(
            qpos=np.array(data["qpos"], dtype=np.float64),
            qvel=np.array(data["qvel"], dtype=np.float64),
            act=np.array(data["act"], dtype=np.float64) if data.get("act") is not None else None,
            qacc_warmstart=np.array(data["qacc_warmstart"], dtype=np.float64) if data.get("qacc_warmstart") is not None else None,
            qfrc_applied=np.array(data["qfrc_applied"], dtype=np.float64) if data.get("qfrc_applied") is not None else None,
            xfrc_applied=np.array(data["xfrc_applied"], dtype=np.float64) if data.get("xfrc_applied") is not None else None,
            ctrl=np.array(data["ctrl"], dtype=np.float64) if data.get("ctrl") is not None else None,
            time=float(data.get("time", 0.0)),
            step_count=int(data.get("step_count", 0)),
            remaining_horizon=int(data.get("remaining_horizon", 0)),
            max_horizon=int(data.get("max_horizon", 100)),
            task_goal=np.array(data["task_goal"], dtype=np.float64) if data.get("task_goal") is not None else None,
            object_pos=np.array(data["object_pos"], dtype=np.float64) if data.get("object_pos") is not None else None,
            object_rot=np.array(data["object_rot"], dtype=np.float64) if data.get("object_rot") is not None else None,
            end_effector_pos=np.array(data["end_effector_pos"], dtype=np.float64) if data.get("end_effector_pos") is not None else None,
            active_contacts_count=int(data.get("active_contacts_count", 0)),
            metadata=dict(data.get("metadata", {})),
        )

    def save(self, filepath: str) -> None:
        """Save snapshot to compressed npz archive."""
        arrays = {
            "qpos": self.qpos,
            "qvel": self.qvel,
        }
        if self.act is not None:
            arrays["act"] = self.act
        if self.qacc_warmstart is not None:
            arrays["qacc_warmstart"] = self.qacc_warmstart
        if self.qfrc_applied is not None:
            arrays["qfrc_applied"] = self.qfrc_applied
        if self.xfrc_applied is not None:
            arrays["xfrc_applied"] = self.xfrc_applied
        if self.ctrl is not None:
            arrays["ctrl"] = self.ctrl
        if self.task_goal is not None:
            arrays["task_goal"] = self.task_goal
        if self.object_pos is not None:
            arrays["object_pos"] = self.object_pos
        if self.object_rot is not None:
            arrays["object_rot"] = self.object_rot
        if self.end_effector_pos is not None:
            arrays["end_effector_pos"] = self.end_effector_pos

        scalars = np.array([
            self.time,
            float(self.step_count),
            float(self.remaining_horizon),
            float(self.max_horizon),
            float(self.active_contacts_count),
        ], dtype=np.float64)
        arrays["__scalars__"] = scalars

        np.savez_compressed(filepath, **arrays)

    @classmethod
    def load(cls, filepath: str) -> StateSnapshot:
        """Load snapshot from compressed npz archive."""
        loaded = np.load(filepath)
        scalars = loaded.get("__scalars__", [0.0, 0.0, 0.0, 100.0, 0.0])
        return cls(
            qpos=loaded["qpos"],
            qvel=loaded["qvel"],
            act=loaded["act"] if "act" in loaded else None,
            qacc_warmstart=loaded["qacc_warmstart"] if "qacc_warmstart" in loaded else None,
            qfrc_applied=loaded["qfrc_applied"] if "qfrc_applied" in loaded else None,
            xfrc_applied=loaded["xfrc_applied"] if "xfrc_applied" in loaded else None,
            ctrl=loaded["ctrl"] if "ctrl" in loaded else None,
            time=float(scalars[0]),
            step_count=int(scalars[1]),
            remaining_horizon=int(scalars[2]),
            max_horizon=int(scalars[3]),
            active_contacts_count=int(scalars[4]),
            task_goal=loaded["task_goal"] if "task_goal" in loaded else None,
            object_pos=loaded["object_pos"] if "object_pos" in loaded else None,
            object_rot=loaded["object_rot"] if "object_rot" in loaded else None,
            end_effector_pos=loaded["end_effector_pos"] if "end_effector_pos" in loaded else None,
        )

    def compute_distance(
        self,
        other: StateSnapshot,
        weights: Optional[Dict[str, float]] = None,
    ) -> float:
        """Compute weighted physical distance d(s1, s2) between two snapshots."""
        w = weights or {
            "qpos": 0.35,
            "qvel": 0.15,
            "object_pos": 0.25,
            "end_effector_pos": 0.15,
            "contact": 0.10,
        }

        d_qpos = float(np.linalg.norm(self.qpos - other.qpos))
        d_qvel = float(np.linalg.norm(self.qvel - other.qvel))

        d_obj = 0.0
        if self.object_pos is not None and other.object_pos is not None:
            d_obj = float(np.linalg.norm(self.object_pos - other.object_pos))

        d_ee = 0.0
        if self.end_effector_pos is not None and other.end_effector_pos is not None:
            d_ee = float(np.linalg.norm(self.end_effector_pos - other.end_effector_pos))

        d_contact = 1.0 if self.active_contacts_count != other.active_contacts_count else 0.0

        total_d = (
            w.get("qpos", 0.35) * d_qpos
            + w.get("qvel", 0.15) * d_qvel
            + w.get("object_pos", 0.25) * d_obj
            + w.get("end_effector_pos", 0.15) * d_ee
            + w.get("contact", 0.10) * d_contact
        )
        return float(total_d)

