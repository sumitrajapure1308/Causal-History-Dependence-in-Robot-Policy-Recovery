"""Rollout Collection Script.

Executes and logs policy rollouts in PushTargetEnv:
- Nominal unperturbed rollouts.
- Induced off-center slip deviation rollouts.
- Saves full per-episode JSON metadata and compressed NPZ trajectory archives.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List
import numpy as np

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.policies.policy_registry import load_policy
from causal_history_recovery.rollout.episode_logger import EpisodeLogger
from causal_history_recovery.rollout.rollout_collector import RolloutCollector


def run_collection(
    policy_type: str = "reactive_mlp",
    num_episodes: int = 20,
    base_seed: int = 42,
    mode: str = "nominal",
    output_dir: str = "results/pilot_recovery/episodes",
) -> List[Dict[str, Any]]:
    """Execute collection run over specified episodes and policy."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    checkpoint_path = os.path.join(repo_root, "models", "checkpoints", f"{policy_type}_best.pt")

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found at {checkpoint_path}. Train policy first.")

    policy = load_policy(checkpoint_path, device="cpu")
    env = PushTargetEnv(max_horizon=150)
    abs_out_dir = os.path.join(repo_root, output_dir)
    logger = EpisodeLogger(abs_out_dir)
    collector = RolloutCollector(env, logger, checkpoint_path=checkpoint_path)

    results = []
    print(f"Collecting {num_episodes} {mode} episodes for {policy_type} (base seed {base_seed})...")
    start_time = time.time()

    for idx in range(num_episodes):
        ep_seed = base_seed + idx * 7  # reproducible seed sequence
        if mode == "nominal":
            res = collector.run_nominal_rollout(
                policy=policy,
                seed=ep_seed,
                policy_id=policy_type,
                condition="nominal",
            )
        elif mode == "induced_deviation":
            res = collector.run_induced_deviation_rollout(
                policy=policy,
                seed=ep_seed,
                policy_id=policy_type,
                perturb_step=25,
                offset_y=0.016,
            )
        else:
            raise ValueError(f"Unknown mode: {mode}")

        results.append(res)
        if (idx + 1) % 5 == 0 or (idx + 1) == num_episodes:
            succ = sum(1 for r in results if r["is_success"])
            print(f"Episode {idx+1:2d}/{num_episodes:2d} | Cumulative Success: {succ}/{idx+1}")

    total_time = time.time() - start_time
    print(f"Collection complete in {total_time:.2f}s. Saved to {abs_out_dir}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=str, default="reactive_mlp", choices=["reactive_mlp", "history_gru"])
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", type=str, default="nominal", choices=["nominal", "induced_deviation"])
    parser.add_argument("--output_dir", type=str, default="results/pilot_recovery/episodes")
    args = parser.parse_args()

    run_collection(
        policy_type=args.policy,
        num_episodes=args.episodes,
        base_seed=args.seed,
        mode=args.mode,
        output_dir=args.output_dir,
    )

