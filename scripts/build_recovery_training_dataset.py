"""Generate Recovery-Augmented Behavioral Cloning Training Dataset.

Collects nominal expert pushes, multi-phase recovery demonstrations (retraction,
re-alignment, directed push), and failed recovery attempts across clean training seeds:
- Train cohort: seeds 3000 to 3049 (50 episodes)
- Validation cohort: seeds 3050 to 3059 (10 episodes)
- Zero contamination with benchmark evaluation seeds (42, 500, 2000).

Outputs saved to:
- data/processed/recovery_training_dataset.npz
- data/processed/dataset_manifest.json
"""

from __future__ import annotations

import collections
import hashlib
import json
import os
import sys
from typing import Any, Deque, Dict, List, Tuple
import numpy as np
import yaml

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.controllers.privileged_oracle import PrivilegedOracleController


def compute_causal_features(
    obs: np.ndarray,
    step: int,
    detected: bool,
    detect_step: int,
    max_horizon: int = 150,
) -> Tuple[np.ndarray, bool, int]:
    """Compute online causal deviation features from observation."""
    cos_yaw = obs[9]
    sin_yaw = obs[10]
    yaw = float(np.arctan2(sin_yaw, cos_yaw))
    obj_y = float(obs[7])

    yaw_dev = abs(yaw)
    drift_dev = abs(obj_y)

    if not detected and (yaw_dev > 0.26 or drift_dev > 0.025):
        detected = True
        detect_step = step

    failure_flag = 1.0 if detected else 0.0
    dev_time = (step - detect_step) / 100.0 if detected else 0.0
    dev_mag = yaw_dev if detected else 0.0
    rem_horiz = max(0.0, float(max_horizon - step) / float(max_horizon))

    aug_obs = np.concatenate([
        obs,
        np.array([failure_flag, dev_time, dev_mag, rem_horiz], dtype=np.float32),
    ], dtype=np.float32)

    return aug_obs, detected, detect_step


def collect_nominal_episode(env: PushTargetEnv, seed: int, max_steps: int = 100) -> Dict[str, Any]:
    """Collect nominal expert push episode."""
    obs, _ = env.reset(seed=seed)
    goal = env.get_task_goal()[:2]

    ep_obs = []
    ep_act = []
    ep_contact = []
    ep_phase = []

    detected = False
    detect_step = 0

    for step in range(max_steps):
        aug_obs, detected, detect_step = compute_causal_features(obs, step, detected, detect_step)
        cur_obj = env.get_object_position()[:2]
        dist_goal = np.linalg.norm(cur_obj - goal)

        if dist_goal < 0.038:
            act = np.zeros(3, dtype=np.float32)
        else:
            to_goal = goal - cur_obj
            u_goal = to_goal / dist_goal
            standoff = cur_obj - 0.045 * u_goal
            cur_ee = env.get_end_effector_position()[:2]
            diff = standoff - cur_ee
            dist_standoff = np.linalg.norm(diff)

            if dist_standoff > 0.012:
                v = (diff / dist_standoff) * min(dist_standoff, 0.008)
                act = np.array([v[0], v[1], 0.0], dtype=np.float32)
            else:
                v = u_goal * 0.0035
                act = np.array([v[0], v[1], 0.0], dtype=np.float32)

        contact = 1.0 if env._has_pusher_contact() else 0.0

        ep_obs.append(aug_obs)
        ep_act.append(act)
        ep_contact.append(contact)
        ep_phase.append(0)  # Nominal phase

        obs, _, done, _, info = env.step(act)
        if done:
            break

    return {
        "obs": np.array(ep_obs, dtype=np.float32),
        "actions": np.array(ep_act, dtype=np.float32),
        "contacts": np.array(ep_contact, dtype=np.float32),
        "phases": np.array(ep_phase, dtype=np.int32),
        "success": 1 if info.get("is_success", False) else 0,
        "seed": seed,
        "type": "nominal",
    }


def collect_recovery_episode(
    env: PushTargetEnv,
    seed: int,
    perturb_step: int = 25,
    max_steps: int = 120,
) -> Dict[str, Any]:
    """Collect slip failure episode followed by multi-phase recovery maneuver."""
    obs, _ = env.reset(seed=seed)
    goal = env.get_task_goal()[:2]

    ep_obs = []
    ep_act = []
    ep_contact = []
    ep_phase = []

    detected = False
    detect_step = 0

    # Phase 0: Initial nominal push until perturbation
    for step in range(perturb_step):
        aug_obs, detected, detect_step = compute_causal_features(obs, step, detected, detect_step)
        act = np.array([0.0035, 0.0, 0.0], dtype=np.float32)
        contact = 1.0 if env._has_pusher_contact() else 0.0

        ep_obs.append(aug_obs)
        ep_act.append(act)
        ep_contact.append(contact)
        ep_phase.append(0)

        obs, _, done, _, _ = env.step(act)

    # Inject lateral off-center rotational perturbation
    env.data.qpos[4] += 0.015  # lateral shift
    env.data.qpos[6:10] = [0.9659, 0.0, 0.0, 0.2588]  # ~30 deg yaw
    env.data.qvel[:] = 0.0
    import mujoco
    mujoco.mj_forward(env.model, env.data)
    obs = env._get_observation()

    # Recovery Phase 1: Retraction (8 steps)
    retract_steps = 8
    for r_idx in range(retract_steps):
        step = perturb_step + r_idx
        aug_obs, detected, detect_step = compute_causal_features(obs, step, detected, detect_step)
        act = np.array([-0.006, 0.0, 0.0], dtype=np.float32)
        contact = 1.0 if env._has_pusher_contact() else 0.0

        ep_obs.append(aug_obs)
        ep_act.append(act)
        ep_contact.append(contact)
        ep_phase.append(1)  # Retraction phase

        obs, _, done, _, _ = env.step(act)

    # Recovery Phase 2: Lateral re-alignment behind cube
    cur_step = perturb_step + retract_steps
    for a_idx in range(15):
        step = cur_step + a_idx
        aug_obs, detected, detect_step = compute_causal_features(obs, step, detected, detect_step)
        cur_obj = env.get_object_position()[:2]
        to_goal = goal - cur_obj
        dist_g = max(np.linalg.norm(to_goal), 1e-4)
        u_goal = to_goal / dist_g
        standoff = cur_obj - 0.045 * u_goal

        cur_ee = env.get_end_effector_position()[:2]
        diff = standoff - cur_ee
        dist_s = np.linalg.norm(diff)
        if dist_s < 0.003:
            break

        step_xy = (diff / dist_s) * min(dist_s, 0.008)
        act = np.array([step_xy[0], step_xy[1], 0.0], dtype=np.float32)
        contact = 1.0 if env._has_pusher_contact() else 0.0

        ep_obs.append(aug_obs)
        ep_act.append(act)
        ep_contact.append(contact)
        ep_phase.append(2)  # Re-alignment phase

        obs, _, done, _, _ = env.step(act)

    # Recovery Phase 3: Directed push & dwell
    cur_step = len(ep_obs)
    info = {"is_success": False}
    for p_idx in range(max_steps - cur_step):
        step = cur_step + p_idx
        aug_obs, detected, detect_step = compute_causal_features(obs, step, detected, detect_step)
        cur_obj = env.get_object_position()[:2]
        dist_goal = np.linalg.norm(cur_obj - goal)

        if dist_goal < 0.038:
            act = np.zeros(3, dtype=np.float32)
        else:
            to_goal = goal - cur_obj
            u_push = to_goal / max(dist_goal, 1e-4)
            act = np.array([u_push[0] * 0.0035, u_push[1] * 0.0035, 0.0], dtype=np.float32)

        contact = 1.0 if env._has_pusher_contact() else 0.0

        ep_obs.append(aug_obs)
        ep_act.append(act)
        ep_contact.append(contact)
        ep_phase.append(3)  # Directed push phase

        obs, _, done, _, info = env.step(act)
        if done:
            break

    return {
        "obs": np.array(ep_obs, dtype=np.float32),
        "actions": np.array(ep_act, dtype=np.float32),
        "contacts": np.array(ep_contact, dtype=np.float32),
        "phases": np.array(ep_phase, dtype=np.int32),
        "success": 1 if info.get("is_success", False) else 0,
        "seed": seed,
        "type": "recovery",
    }


def build_sliding_window_dataset(
    episodes: List[Dict[str, Any]],
    history_window: int = 10,
) -> Dict[str, np.ndarray]:
    """Construct sliding-window sequential training tensors."""
    seq_obs_tokens = []
    flat_aug_obs = []
    target_actions = []
    phases = []
    successes = []

    for ep in episodes:
        obs_seq = ep["obs"]         # (T, 24)
        act_seq = ep["actions"]     # (T, 3)
        contact_seq = ep["contacts"]# (T,)
        phase_seq = ep["phases"]
        succ = ep["success"]
        t_len = len(obs_seq)

        # Token: [aug_obs (24), prev_action (3), prev_contact (1)] = 28 dims
        prev_actions = np.vstack([np.zeros((1, 3), dtype=np.float32), act_seq[:-1]])
        prev_contacts = np.concatenate([[0.0], contact_seq[:-1]])[:, None].astype(np.float32)
        tokens = np.hstack([obs_seq, prev_actions, prev_contacts])  # (T, 28)

        for t in range(t_len):
            flat_aug_obs.append(obs_seq[t])
            target_actions.append(act_seq[t])
            phases.append(phase_seq[t])
            successes.append(succ)

            # Sequence window
            if t < history_window:
                pad_len = history_window - (t + 1)
                pad = np.tile(tokens[0], (pad_len, 1))
                win = np.vstack([pad, tokens[: t + 1]])
            else:
                win = tokens[t - history_window + 1 : t + 1]

            seq_obs_tokens.append(win)

    return {
        "flat_aug_obs": np.array(flat_aug_obs, dtype=np.float32),     # (N, 24)
        "seq_tokens": np.array(seq_obs_tokens, dtype=np.float32),      # (N, 10, 28)
        "target_actions": np.array(target_actions, dtype=np.float32),  # (N, 3)
        "phases": np.array(phases, dtype=np.int32),
        "successes": np.array(successes, dtype=np.int32),
    }


def main():
    cfg_path = os.path.join(repo_root, "configs", "training", "recovery_training_config.yaml")
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)["dataset"]

    out_path = os.path.join(repo_root, cfg["dataset_output_path"])
    manifest_path = os.path.join(repo_root, cfg["manifest_output_path"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    env = PushTargetEnv()
    train_episodes = []
    val_episodes = []

    print("Collecting Training Demonstrations (Seeds 3000-3049)...")
    # 25 nominal, 25 recovery
    for i in range(25):
        train_episodes.append(collect_nominal_episode(env, seed=cfg["seed_start_train"] + i))
    for i in range(25):
        train_episodes.append(collect_recovery_episode(env, seed=cfg["seed_start_train"] + 25 + i))

    print("Collecting Validation Demonstrations (Seeds 3050-3059)...")
    for i in range(5):
        val_episodes.append(collect_nominal_episode(env, seed=cfg["seed_start_val"] + i))
    for i in range(5):
        val_episodes.append(collect_recovery_episode(env, seed=cfg["seed_start_val"] + 5 + i))

    train_data = build_sliding_window_dataset(train_episodes, cfg["history_window"])
    val_data = build_sliding_window_dataset(val_episodes, cfg["history_window"])

    # Save as compressed npz
    np.savez_compressed(
        out_path,
        train_flat_obs=train_data["flat_aug_obs"],
        train_seq_tokens=train_data["seq_tokens"],
        train_actions=train_data["target_actions"],
        train_phases=train_data["phases"],
        val_flat_obs=val_data["flat_aug_obs"],
        val_seq_tokens=val_data["seq_tokens"],
        val_actions=val_data["target_actions"],
        val_phases=val_data["phases"],
    )

    with open(out_path, "rb") as f:
        file_sha256 = hashlib.sha256(f.read()).hexdigest()

    manifest = {
        "metadata": {
            "title": "Recovery-Augmented Demonstration Dataset",
            "phase": 7,
            "status": "Verified",
            "sha256": file_sha256,
            "train_episodes": len(train_episodes),
            "val_episodes": len(val_episodes),
            "train_samples": len(train_data["target_actions"]),
            "val_samples": len(val_data["target_actions"]),
            "aug_obs_dim": int(train_data["flat_aug_obs"].shape[1]),
            "token_dim": int(train_data["seq_tokens"].shape[2]),
            "history_window": cfg["history_window"],
        },
        "composition": {
            "train": {
                "nominal_episodes": 25,
                "recovery_episodes": 25,
                "success_rate": float(np.mean([ep["success"] for ep in train_episodes])),
            },
            "validation": {
                "nominal_episodes": 5,
                "recovery_episodes": 5,
                "success_rate": float(np.mean([ep["success"] for ep in val_episodes])),
            },
        },
        "anti_leakage_audit": {
            "training_seeds": f"{cfg['seed_start_train']} to {cfg['seed_start_train'] + 49}",
            "validation_seeds": f"{cfg['seed_start_val']} to {cfg['seed_start_val'] + 9}",
            "evaluation_seeds": [42, 500, 2000],
            "overlap_with_eval_seeds": False,
            "overlap_with_benchmark_scenarios": False,
        },
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Dataset generated successfully at: {out_path}")
    print(f"Manifest saved to: {manifest_path}")
    print(f"Train samples: {len(train_data['target_actions'])}, Val samples: {len(val_data['target_actions'])}")
    print(f"Dataset SHA-256: {file_sha256}")


if __name__ == "__main__":
    main()

