"""Policy Training Pipeline via Behavioral Cloning.

Trains Reactive MLP and History-Aware GRU policies from nominal expert demonstrations:
- Behavioral cloning / deterministic imitation objective (MSE on actions).
- Fixed seed control and strict train/val split (80/20).
- No test-set leakage (demonstration seeds starting at 1000+, evaluation at 42+).
- Saves model checkpoints to models/checkpoints/.
- Saves training curves and logs to results/training_logs/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Tuple
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import yaml

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.policies.policy_registry import create_policy


def collect_expert_demonstrations(
    num_episodes: int = 50,
    seed_start: int = 1000,
    max_steps_per_episode: int = 100,
) -> List[Dict[str, np.ndarray]]:
    """Collect nominal expert demonstrations using the geometric nominal controller."""
    env = PushTargetEnv()
    demonstrations = []

    for ep_idx in range(num_episodes):
        ep_seed = seed_start + ep_idx
        obs, info = env.reset(seed=ep_seed)
        goal = env.get_task_goal()[:2]

        ep_obs = []
        ep_act = []

        for _ in range(max_steps_per_episode):
            ee_pos = env.get_end_effector_position()[:2]
            obj_pos = env.get_object_position()[:2]
            dist_goal = np.linalg.norm(obj_pos - goal)

            if dist_goal < 0.040:
                act = np.zeros(3, dtype=np.float32)
            else:
                to_goal = goal - obj_pos
                u_goal = to_goal / dist_goal
                standoff = obj_pos - 0.045 * u_goal
                diff = standoff - ee_pos
                dist_ee = np.linalg.norm(diff)

                if dist_ee > 0.008 and ee_pos[0] < obj_pos[0] - 0.035:
                    step_xy = (diff / dist_ee) * min(dist_ee, 0.006)
                    act = np.array([step_xy[0], step_xy[1], 0.0], dtype=np.float32)
                else:
                    desired = obj_pos - 0.025 * u_goal
                    diff_push = desired - ee_pos
                    dist_push = np.linalg.norm(diff_push)
                    step_xy = (diff_push / max(dist_push, 1e-4)) * min(dist_push, 0.004)
                    act = np.array([step_xy[0], step_xy[1], 0.0], dtype=np.float32)

            ep_obs.append(obs.copy())
            ep_act.append(act.copy())

            obs, r, term, trunc, step_info = env.step(act)
            if step_info["is_success"]:
                break
            if term or trunc:
                break

        demonstrations.append({
            "observations": np.array(ep_obs, dtype=np.float32),
            "actions": np.array(ep_act, dtype=np.float32),
        })

    return demonstrations


def build_training_tensors(
    demonstrations: List[Dict[str, np.ndarray]],
    policy_type: str,
    history_window: int = 10,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Convert demonstrations to PyTorch tensors for MLP or GRU training."""
    if policy_type == "reactive_mlp":
        all_obs = np.concatenate([d["observations"] for d in demonstrations], axis=0)
        all_act = np.concatenate([d["actions"] for d in demonstrations], axis=0)
        return torch.from_numpy(all_obs), torch.from_numpy(all_act)

    elif policy_type == "history_gru":
        seq_inputs = []
        target_actions = []

        for d in demonstrations:
            obs_seq = d["observations"]
            act_seq = d["actions"]
            t_len = len(obs_seq)
            if t_len == 0:
                continue

            # Prepend zero action for the first timestep
            prev_act_seq = np.vstack([np.zeros((1, 3), dtype=np.float32), act_seq[:-1]])
            tokens = np.hstack([obs_seq, prev_act_seq])  # (T, 23)

            for t in range(t_len):
                if t < history_window:
                    pad_len = history_window - (t + 1)
                    pad = np.tile(tokens[0], (pad_len, 1))
                    window = np.vstack([pad, tokens[: t + 1]])
                else:
                    window = tokens[t - history_window + 1 : t + 1]

                seq_inputs.append(window)
                target_actions.append(act_seq[t])

        return torch.from_numpy(np.array(seq_inputs, dtype=np.float32)), torch.from_numpy(
            np.array(target_actions, dtype=np.float32)
        )

    else:
        raise ValueError(f"Unknown policy type: {policy_type}")


def train_policy(
    policy_type: str = "reactive_mlp",
    config_path: Optional[str] = None,
    epochs: int = 30,
    seed: int = 42,
    batch_size: int = 32,
    lr: float = 0.001,
) -> Dict[str, Any]:
    """Train policy model via behavioral cloning and save checkpoint."""
    torch.manual_seed(seed)
    np.random.seed(seed)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Load policy config
    if config_path is None:
        config_path = os.path.join(repo_root, "configs", "policies", f"{policy_type}.yaml")
    
    with open(config_path, "r", encoding="utf-8") as f:
        policy_config = yaml.safe_load(f)

    policy = create_policy(policy_type, policy_config)
    history_window = policy_config.get("history_window", 10)

    # Collect demonstration data
    print(f"Collecting 50 nominal expert demonstrations starting at seed 1000...")
    demos = collect_expert_demonstrations(num_episodes=50, seed_start=1000)

    inputs, targets = build_training_tensors(demos, policy_type, history_window)
    total_samples = len(inputs)
    split_idx = int(0.8 * total_samples)

    # Random permutation with fixed seed
    perm = torch.randperm(total_samples)
    train_indices = perm[:split_idx]
    val_indices = perm[split_idx:]

    train_dataset = TensorDataset(inputs[train_indices], targets[train_indices])
    val_dataset = TensorDataset(inputs[val_indices], targets[val_indices])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    optimizer = torch.optim.Adam(
        policy.model.parameters(),
        lr=lr,
        weight_decay=1e-5,
    )
    criterion = nn.MSELoss()

    history_log = {
        "policy_type": policy_type,
        "seed": seed,
        "epochs": epochs,
        "train_samples": len(train_indices),
        "val_samples": len(val_indices),
        "history": [],
    }

    best_val_loss = float("inf")
    checkpoint_dir = os.path.join(repo_root, "models", "checkpoints")
    os.makedirs(checkpoint_dir, exist_ok=True)
    best_checkpoint_path = os.path.join(checkpoint_dir, f"{policy_type}_best.pt")

    print(f"Starting training for {policy_type} ({epochs} epochs, {len(train_indices)} train, {len(val_indices)} val)...")
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        policy.model.train()
        train_losses = []
        for x_b, y_b in train_loader:
            optimizer.zero_grad()
            if policy_type == "reactive_mlp":
                pred = policy.model(x_b)
            else:
                pred, _ = policy.model(x_b)
                pred = pred[:, -1, :]  # Predict action at final window step

            loss = criterion(pred, y_b)
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        policy.model.eval()
        val_losses = []
        with torch.no_grad():
            for x_v, y_v in val_loader:
                if policy_type == "reactive_mlp":
                    pred_v = policy.model(x_v)
                else:
                    pred_v, _ = policy.model(x_v)
                    pred_v = pred_v[:, -1, :]
                val_losses.append(criterion(pred_v, y_v).item())

        mean_train = float(np.mean(train_losses))
        mean_val = float(np.mean(val_losses))

        history_log["history"].append({
            "epoch": epoch,
            "train_loss": mean_train,
            "val_loss": mean_val,
        })

        if mean_val < best_val_loss:
            best_val_loss = mean_val
            policy.save(best_checkpoint_path)

        if epoch % 5 == 0 or epoch == epochs:
            print(f"Epoch {epoch:2d}/{epochs:2d} | Train MSE: {mean_train:.6f} | Val MSE: {mean_val:.6f} | Best: {best_val_loss:.6f}")

    total_time = time.time() - start_time
    history_log["best_val_loss"] = float(best_val_loss)
    history_log["training_time_seconds"] = float(total_time)
    history_log["best_checkpoint_path"] = best_checkpoint_path

    # Save log
    log_dir = os.path.join(repo_root, "results", "training_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{policy_type}_training_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(history_log, f, indent=2)

    print(f"Training completed in {total_time:.2f}s. Checkpoint saved to {best_checkpoint_path}")
    print(f"Training log saved to {log_path}")
    return history_log


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=str, default="reactive_mlp", choices=["reactive_mlp", "history_gru"])
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train_policy(policy_type=args.policy, epochs=args.epochs, seed=args.seed)

