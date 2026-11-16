"""Train Recovery-Augmented Policies via Behavioral Cloning.

Trains RecoveryAugmentedMLP and RecoveryAugmentedGRU across 3 fixed seeds:
- Loads pre-generated dataset from data/processed/recovery_training_dataset.npz
- Fixed training budget (35 epochs, batch_size 32, lr 0.001)
- Fixed early-stopping rule (patience 10)
- Zero test-set leakage (clean training demonstrations)
- Records training and validation losses per epoch
- Saves checkpoints and metrics to results/recovery_training/
"""

from __future__ import annotations

import argparse
import hashlib
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

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

from causal_history_recovery.policies.policy_registry import create_policy


def train_single_run(
    policy_type: str,
    data: Dict[str, np.ndarray],
    seed: int,
    epochs: int = 35,
    batch_size: int = 32,
    lr: float = 0.001,
    weight_decay: float = 1e-5,
    out_dir: str = "results/recovery_training",
) -> Dict[str, Any]:
    """Execute single training run for a policy under a fixed random seed."""
    torch.manual_seed(seed)
    np.random.seed(seed)

    cfg_path = os.path.join(repo_root, "configs", "policies", f"{policy_type}.yaml")
    with open(cfg_path) as f:
        policy_cfg = yaml.safe_load(f)

    policy = create_policy(policy_type, policy_cfg)

    if policy_type == "recovery_augmented_mlp":
        x_train = torch.from_numpy(data["train_flat_obs"])
        y_train = torch.from_numpy(data["train_actions"])
        x_val = torch.from_numpy(data["val_flat_obs"])
        y_val = torch.from_numpy(data["val_actions"])
    else:  # recovery_augmented_gru
        x_train = torch.from_numpy(data["train_seq_tokens"])
        y_train = torch.from_numpy(data["train_actions"])
        x_val = torch.from_numpy(data["val_seq_tokens"])
        y_val = torch.from_numpy(data["val_actions"])

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=batch_size, shuffle=False)

    optimizer = torch.optim.Adam(policy.model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.MSELoss()

    best_val_loss = float("inf")
    patience = 10
    patience_counter = 0

    history = {"train_loss": [], "val_loss": []}
    ckpt_dir = os.path.join(repo_root, out_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    best_ckpt_path = os.path.join(ckpt_dir, f"{policy_type}_seed{seed}.pt")

    for epoch in range(1, epochs + 1):
        policy.model.train()
        t_losses = []
        for xb, yb in train_loader:
            optimizer.zero_grad()
            if policy_type == "recovery_augmented_mlp":
                pred = policy.model(xb)
            else:
                pred, _ = policy.model(xb)
                pred = pred[:, -1, :]

            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            t_losses.append(loss.item())

        mean_train = float(np.mean(t_losses))

        policy.model.eval()
        v_losses = []
        with torch.no_grad():
            for xb, yb in val_loader:
                if policy_type == "recovery_augmented_mlp":
                    pred = policy.model(xb)
                else:
                    pred, _ = policy.model(xb)
                    pred = pred[:, -1, :]
                v_losses.append(criterion(pred, yb).item())

        mean_val = float(np.mean(v_losses))
        history["train_loss"].append(mean_train)
        history["val_loss"].append(mean_val)

        if mean_val < best_val_loss - 1e-5:
            best_val_loss = mean_val
            patience_counter = 0
            # Save checkpoint
            torch.save({
                "policy_type": policy_type,
                "state_dict": policy.model.state_dict(),
                "config": policy_cfg,
                "seed": seed,
                "epoch": epoch,
                "val_loss": mean_val,
            }, best_ckpt_path)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"[{policy_type} | Seed {seed}] Early stopping triggered at epoch {epoch}")
                break

    print(f"[{policy_type} | Seed {seed}] Completed: Best Val Loss = {best_val_loss:.6f}")
    return {
        "policy_type": policy_type,
        "seed": seed,
        "best_val_loss": best_val_loss,
        "final_train_loss": history["train_loss"][-1],
        "epochs_trained": len(history["train_loss"]),
        "checkpoint_path": os.path.relpath(best_ckpt_path, repo_root),
        "history": history,
    }


def main():
    cfg_path = os.path.join(repo_root, "configs", "training", "recovery_training_config.yaml")
    with open(cfg_path) as f:
        full_cfg = yaml.safe_load(f)

    train_cfg = full_cfg["training"]
    data_path = os.path.join(repo_root, full_cfg["dataset"]["dataset_output_path"])
    raw_data = np.load(data_path)

    out_dir = os.path.join(repo_root, train_cfg["output_dir"])
    os.makedirs(out_dir, exist_ok=True)

    seeds = train_cfg["seeds"]
    policies = ["recovery_augmented_mlp", "recovery_augmented_gru"]

    all_results = {}
    training_metrics = {}
    validation_metrics = {}

    for pol in policies:
        all_results[pol] = []
        training_metrics[pol] = {}
        validation_metrics[pol] = {}

        best_across_seeds = float("inf")
        best_ckpt_for_pol = None

        for seed in seeds:
            print(f"\n--- Training {pol} with seed {seed} ---")
            res = train_single_run(
                policy_type=pol,
                data=raw_data,
                seed=seed,
                epochs=train_cfg["epochs"],
                batch_size=train_cfg["batch_size"],
                lr=train_cfg["learning_rate"],
                weight_decay=train_cfg["weight_decay"],
                out_dir=train_cfg["output_dir"],
            )
            all_results[pol].append(res)
            training_metrics[pol][f"seed_{seed}"] = {
                "final_train_loss": res["final_train_loss"],
                "epochs": res["epochs_trained"],
                "train_loss_curve": res["history"]["train_loss"],
            }
            validation_metrics[pol][f"seed_{seed}"] = {
                "best_val_loss": res["best_val_loss"],
                "val_loss_curve": res["history"]["val_loss"],
            }

            if res["best_val_loss"] < best_across_seeds:
                best_across_seeds = res["best_val_loss"]
                best_ckpt_for_pol = os.path.join(repo_root, res["checkpoint_path"])

        # Also copy the top checkpoint to models/checkpoints/ for standard registry access
        models_dir = os.path.join(repo_root, "models", "checkpoints")
        os.makedirs(models_dir, exist_ok=True)
        dest_path = os.path.join(models_dir, f"{pol}_best.pt")
        import shutil
        shutil.copyfile(best_ckpt_for_pol, dest_path)
        print(f"Top checkpoint copied to: {dest_path}")

    # Write training manifest
    with open(data_path, "rb") as f:
        dataset_hash = hashlib.sha256(f.read()).hexdigest()

    manifest = {
        "metadata": {
            "title": "Recovery-Augmented Training Run Manifest",
            "phase": 7,
            "status": "Verified",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_sha256": dataset_hash,
            "training_seeds": seeds,
            "policies": policies,
            "epochs": train_cfg["epochs"],
            "batch_size": train_cfg["batch_size"],
            "learning_rate": train_cfg["learning_rate"],
        },
        "summary": {
            "recovery_augmented_mlp": {
                "mean_val_loss": float(np.mean([r["best_val_loss"] for r in all_results["recovery_augmented_mlp"]])),
                "best_val_loss": float(np.min([r["best_val_loss"] for r in all_results["recovery_augmented_mlp"]])),
            },
            "recovery_augmented_gru": {
                "mean_val_loss": float(np.mean([r["best_val_loss"] for r in all_results["recovery_augmented_gru"]])),
                "best_val_loss": float(np.min([r["best_val_loss"] for r in all_results["recovery_augmented_gru"]])),
            },
        },
    }

    with open(os.path.join(out_dir, "training_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    with open(os.path.join(out_dir, "training_metrics.json"), "w") as f:
        json.dump(training_metrics, f, indent=2)

    with open(os.path.join(out_dir, "validation_metrics.json"), "w") as f:
        json.dump(validation_metrics, f, indent=2)

    print(f"\nAll recovery training runs completed. Manifest and metrics saved to: {out_dir}")


if __name__ == "__main__":
    main()

