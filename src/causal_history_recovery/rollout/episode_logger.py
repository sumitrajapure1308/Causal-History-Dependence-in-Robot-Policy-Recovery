"""Episode Logger for Causal History Recovery Rollouts.

Serializes comprehensive per-episode trajectory logs:
- Structured JSON metadata (seed, condition, hashes, metrics, deviation labels).
- Compressed NumPy array archives (.npz) storing full observation, action,
  physical-state, and contact-force sequences.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional
import numpy as np


def _json_default(obj: Any) -> Any:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return str(obj)


class EpisodeLogger:
    """Manages serialization of individual episode rollouts with strict provenance."""

    def __init__(self, base_output_dir: str):
        self.base_output_dir = os.path.abspath(base_output_dir)
        os.makedirs(self.base_output_dir, exist_ok=True)

    def log_episode(
        self,
        *,
        run_id: str,
        policy_id: str,
        task_id: str,
        condition: str,
        seed: int,
        checkpoint_path: str,
        env_config: Dict[str, Any],
        policy_config: Dict[str, Any],
        observations: List[np.ndarray],
        actions: List[np.ndarray],
        physical_states: List[np.ndarray],
        rewards: List[float],
        contacts: List[Dict[str, Any]],
        initial_state_dict: Dict[str, Any],
        final_state_dict: Dict[str, Any],
        is_success: bool,
        dwell_count: int,
        remaining_horizon: int,
        deviation_time: Optional[int] = None,
        deviation_type: Optional[str] = None,
        deviation_magnitude: Optional[float] = None,
        recoverability_label: Optional[bool] = None,
        recovery_outcome: Optional[bool] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """Save episode metadata (JSON) and numerical trajectory (.npz)."""
        ep_dir = os.path.join(self.base_output_dir, policy_id, condition)
        os.makedirs(ep_dir, exist_ok=True)

        ep_stem = f"{policy_id}_{condition}_seed{seed}_{run_id}"
        json_path = os.path.join(ep_dir, f"{ep_stem}_meta.json")
        npz_path = os.path.join(ep_dir, f"{ep_stem}_trajectory.npz")

        # Config hashes for reproducibility
        env_hash = hashlib.sha256(json.dumps(env_config, sort_keys=True).encode()).hexdigest()[:16]
        pol_hash = hashlib.sha256(json.dumps(policy_config, sort_keys=True).encode()).hexdigest()[:16]

        meta = {
            "run_id": run_id,
            "policy_id": policy_id,
            "task_id": task_id,
            "condition": condition,
            "seed": int(seed),
            "checkpoint_path": checkpoint_path,
            "env_config_hash": env_hash,
            "policy_config_hash": pol_hash,
            "episode_length": len(actions),
            "final_task_success": bool(is_success),
            "dwell_count": int(dwell_count),
            "remaining_horizon": int(remaining_horizon),
            "deviation_time": int(deviation_time) if deviation_time is not None else None,
            "deviation_type": deviation_type,
            "deviation_magnitude": float(deviation_magnitude) if deviation_magnitude is not None else None,
            "recoverability_label": bool(recoverability_label) if recoverability_label is not None else None,
            "recovery_outcome": bool(recovery_outcome) if recovery_outcome is not None else None,
            "initial_state": initial_state_dict,
            "final_state": final_state_dict,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "trajectory_npz_path": os.path.relpath(npz_path, self.base_output_dir),
            "extra_metadata": extra_metadata or {},
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, default=_json_default)

        # Save numerical sequences as compressed NumPy archive
        np.savez_compressed(
            npz_path,
            observations=np.array(observations, dtype=np.float32),
            actions=np.array(actions, dtype=np.float32),
            physical_states=np.array(physical_states, dtype=np.float64),
            rewards=np.array(rewards, dtype=np.float32),
        )

        return {
            "meta_json": json_path,
            "trajectory_npz": npz_path,
        }
