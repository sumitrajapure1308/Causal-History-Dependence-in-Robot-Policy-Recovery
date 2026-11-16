"""Rollout Collector for Causal History Recovery Experiments.

Executes deterministic closed-loop policy rollouts under nominal, deviation-induced,
and counterfactual recovery conditions (B0, B1, B2, B3, B4).
"""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.base_policy import BasePolicy
from causal_history_recovery.rollout.episode_logger import EpisodeLogger
from causal_history_recovery.counterfactuals.condition_generator import ConditionGenerator


class RolloutCollector:
    """Manages policy evaluation rollouts and condition execution."""

    def __init__(
        self,
        env: PushTargetEnv,
        logger: EpisodeLogger,
        checkpoint_path: str = "models/checkpoints/default.pt",
    ):
        self.env = env
        self.logger = logger
        self.checkpoint_path = checkpoint_path

    def run_nominal_rollout(
        self,
        policy: BasePolicy,
        seed: int,
        policy_id: str = "policy",
        condition: str = "nominal",
    ) -> Dict[str, Any]:
        """Execute a standard unperturbed nominal episode."""
        obs, info = self.env.reset(seed=seed)
        policy.reset(obs)

        run_id = str(uuid.uuid4())[:8]
        observations = [obs.copy()]
        actions = []
        physical_states = [self.env.get_physical_state()]
        rewards = []
        contacts_log = []

        is_success = False

        for step in range(self.env._max_horizon):
            action = policy.act(obs, deterministic=True)
            actions.append(action.copy())

            obs, reward, terminated, truncated, step_info = self.env.step(action)
            observations.append(obs.copy())
            physical_states.append(self.env.get_physical_state())
            rewards.append(float(reward))

            # Log contacts
            contacts = self.env.get_contacts()
            contacts_log.append({
                "step": step,
                "count": len(contacts),
                "has_pusher_contact": step_info["has_pusher_contact"],
            })

            if step_info["is_success"]:
                is_success = True
                break
            if terminated or truncated:
                break

        final_snap = self.env.get_state_snapshot()

        log_res = self.logger.log_episode(
            run_id=run_id,
            policy_id=policy_id,
            task_id="planned_custom_push_target_env",
            condition=condition,
            seed=seed,
            checkpoint_path=self.checkpoint_path,
            env_config=self.env.get_environment_metadata(),
            policy_config=policy.get_config(),
            observations=observations,
            actions=actions,
            physical_states=physical_states,
            rewards=rewards,
            contacts=contacts_log,
            initial_state_dict={"seed": seed},
            final_state_dict=final_snap.to_dict(),
            is_success=is_success,
            dwell_count=step_info.get("dwell_count", 0),
            remaining_horizon=self.env.remaining_horizon,
            deviation_time=None,
            deviation_type=None,
            deviation_magnitude=None,
            recoverability_label=None,
            recovery_outcome=None,
        )

        return {
            "run_id": run_id,
            "seed": seed,
            "is_success": is_success,
            "dwell_count": step_info.get("dwell_count", 0),
            "steps": len(actions),
            "final_dist_to_goal": float(step_info.get("dist_to_goal", 0.0)),
            "log_files": log_res,
        }

    def run_induced_deviation_rollout(
        self,
        policy: BasePolicy,
        seed: int,
        policy_id: str = "policy",
        perturb_step: int = 25,
        offset_y: float = 0.016,
    ) -> Dict[str, Any]:
        """Execute episode that induces an off-center contact slip deviation."""
        obs, info = self.env.reset(seed=seed)
        policy.reset(obs)

        run_id = str(uuid.uuid4())[:8]
        observations = [obs.copy()]
        actions = []
        physical_states = [self.env.get_physical_state()]
        rewards = []
        contacts_log = []

        is_success = False
        deviation_detected = False
        deviation_time = None
        yaw_at_dev = 0.0
        drift_at_dev = 0.0
        candidate_snapshot = None

        obj_init = self.env.get_object_position().copy()

        for step in range(self.env._max_horizon):
            if step == perturb_step and not deviation_detected:
                # Apply lateral displacement offset to induce off-center contact
                action = np.array([0.0, offset_y, 0.0], dtype=np.float32)
            else:
                action = policy.act(obs, deterministic=True)

            actions.append(action.copy())

            obs, reward, terminated, truncated, step_info = self.env.step(action)
            observations.append(obs.copy())
            physical_states.append(self.env.get_physical_state())
            rewards.append(float(reward))

            # Monitor slip deviation threshold: yaw >= 15 deg, drift >= 2 cm
            yaw_deg = abs(np.degrees(self.env.get_object_yaw()))
            drift_m = abs(self.env.get_object_position()[1] - obj_init[1])

            if step >= perturb_step and not deviation_detected:
                if yaw_deg >= 15.0 and drift_m >= 0.020:
                    deviation_detected = True
                    deviation_time = step
                    yaw_at_dev = yaw_deg
                    drift_at_dev = drift_m
                    candidate_snapshot = self.env.get_state_snapshot()

            contacts = self.env.get_contacts()
            contacts_log.append({
                "step": step,
                "count": len(contacts),
                "has_pusher_contact": step_info["has_pusher_contact"],
            })

            if step_info["is_success"]:
                is_success = True
                break
            if terminated or truncated:
                break

        final_snap = self.env.get_state_snapshot()

        log_res = self.logger.log_episode(
            run_id=run_id,
            policy_id=policy_id,
            task_id="planned_custom_push_target_env",
            condition="induced_deviation",
            seed=seed,
            checkpoint_path=self.checkpoint_path,
            env_config=self.env.get_environment_metadata(),
            policy_config=policy.get_config(),
            observations=observations,
            actions=actions,
            physical_states=physical_states,
            rewards=rewards,
            contacts=contacts_log,
            initial_state_dict={"seed": seed},
            final_state_dict=final_snap.to_dict(),
            is_success=is_success,
            dwell_count=step_info.get("dwell_count", 0),
            remaining_horizon=self.env.remaining_horizon,
            deviation_time=deviation_time,
            deviation_type="off_center_slip" if deviation_detected else None,
            deviation_magnitude=yaw_at_dev,
            recoverability_label=None,
            recovery_outcome=is_success,
            extra_metadata={
                "drift_at_dev_m": drift_at_dev,
                "perturb_step": perturb_step,
                "offset_y": offset_y,
            },
        )

        return {
            "run_id": run_id,
            "seed": seed,
            "is_success": is_success,
            "deviation_detected": deviation_detected,
            "deviation_time": deviation_time,
            "yaw_at_dev": yaw_at_dev,
            "drift_at_dev": drift_at_dev,
            "candidate_snapshot": candidate_snapshot,
            "prefix_actions": actions[:deviation_time] if deviation_time is not None else [],
            "log_files": log_res,
        }

    def run_recovery_condition_rollout(
        self,
        policy: BasePolicy,
        source_snapshot: StateSnapshot,
        action_prefix: List[np.ndarray],
        condition: str,
        seed: int,
        policy_id: str = "policy",
        alternative_memory_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute recovery rollout under an explicit or legacy counterfactual condition."""
        gen = ConditionGenerator(self.env)
        setup_info = gen.prepare_condition_rollout(
            condition=condition,
            policy=policy,
            source_snapshot=source_snapshot,
            action_prefix=action_prefix,
            seed=seed,
            alternative_memory_state=alternative_memory_state,
        )

        obs = setup_info["current_observation"]
        run_id = str(uuid.uuid4())[:8]
        observations = [obs.copy()]
        actions = []
        physical_states = [self.env.get_physical_state()]
        rewards = []
        contacts_log = []

        is_success = False
        rem_h = self.env.remaining_horizon
        recovery_time = float(rem_h)

        for step in range(rem_h):
            action = policy.act(obs, deterministic=True)
            actions.append(action.copy())

            obs, reward, terminated, truncated, step_info = self.env.step(action)
            observations.append(obs.copy())
            physical_states.append(self.env.get_physical_state())
            rewards.append(float(reward))

            contacts = self.env.get_contacts()
            contacts_log.append({
                "step": step,
                "count": len(contacts),
                "has_pusher_contact": step_info.get("has_pusher_contact", False),
            })

            if step_info.get("is_success", False):
                is_success = True
                recovery_time = float(step + 1)
                break
            if terminated or truncated:
                break

        final_snap = self.env.get_state_snapshot()

        log_res = self.logger.log_episode(
            run_id=run_id,
            policy_id=policy_id,
            task_id=self.env.get_environment_metadata().get("env_id", "push_target_env"),
            condition=condition,
            seed=seed,
            checkpoint_path=self.checkpoint_path,
            env_config=self.env.get_environment_metadata(),
            policy_config=policy.get_config(),
            observations=observations,
            actions=actions,
            physical_states=physical_states,
            rewards=rewards,
            contacts=contacts_log,
            initial_state_dict={"seed": seed, "snapshot_qpos": source_snapshot.qpos.tolist()},
            final_state_dict=final_snap.to_dict(),
            is_success=is_success,
            dwell_count=step_info.get("dwell_count", 0),
            remaining_horizon=self.env.remaining_horizon,
            deviation_time=None,
            deviation_type=None,
            deviation_magnitude=None,
            recoverability_label=None,
            recovery_outcome=is_success,
            extra_metadata={
                "memory_condition": condition,
                "canonical_memory_condition": setup_info.get("canonical_memory_condition", condition),
                "execution_mode": setup_info.get("execution_mode", "injection"),
                "state_matching_error": setup_info.get("state_matching_error", 0.0),
                "initial_hidden_norm": setup_info.get("initial_hidden_norm", 0.0),
                "recovery_time": recovery_time,
                "final_dist_to_goal": float(step_info.get("dist_to_goal", 0.0)),
            },
        )

        return {
            "run_id": run_id,
            "seed": seed,
            "condition": condition,
            "canonical_memory_condition": setup_info.get("canonical_memory_condition", condition),
            "is_success": is_success,
            "recovery_time": recovery_time,
            "steps": len(actions),
            "final_dist_to_goal": float(step_info.get("dist_to_goal", 0.0)),
            "state_matching_error": setup_info.get("state_matching_error", 0.0),
            "initial_hidden_norm": setup_info.get("initial_hidden_norm", 0.0),
            "log_files": log_res,
        }


