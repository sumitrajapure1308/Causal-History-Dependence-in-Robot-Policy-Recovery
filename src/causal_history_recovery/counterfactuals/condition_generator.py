"""Condition Generator for Causal History Interventions and Explicit Memory Control.

Provides explicit, clearly named memory and injection conditions:
- M_REPLAY_PRESERVED: Replay execution prefix with preserved policy memory unrolling.
- M_INJECT_PRESERVED: Matched-state injection with preserved policy memory (h != 0).
- M_INJECT_RESET: Matched-state injection with reset policy memory (h = 0).
- M_INJECT_ALTERNATIVE: Matched-state injection with alternative compatible memory (h_alt).

Also maintains full backward compatibility for legacy conditions (B0, B1, B2, B3, B4).
"""

from __future__ import annotations

import copy
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import torch

from causal_history_recovery.environments.push_target_env import PushTargetEnv
from causal_history_recovery.environments.state_snapshot import StateSnapshot
from causal_history_recovery.policies.base_policy import BasePolicy


# Explicit Memory Condition Identifiers
COND_REPLAY_PRESERVED = "M_REPLAY_PRESERVED"
COND_INJECT_PRESERVED = "M_INJECT_PRESERVED"
COND_INJECT_RESET = "M_INJECT_RESET"
COND_INJECT_ALTERNATIVE = "M_INJECT_ALTERNATIVE"


class ConditionGenerator:
    """Configures environment and policy states for counterfactual condition rollouts."""

    def __init__(self, env: PushTargetEnv):
        self.env = env

    def unroll_policy_memory_on_prefix(
        self,
        policy: BasePolicy,
        seed: int,
        action_prefix: List[np.ndarray],
    ) -> Dict[str, Any]:
        """Unroll policy over the deterministic action prefix to extract preserved memory state."""
        obs, info = self.env.reset(seed=seed)
        policy.reset_memory(obs)

        for act in action_prefix:
            policy.act(obs, deterministic=True)
            obs, r, term, trunc, info = self.env.step(act)

        return policy.get_memory_state()

    def prepare_condition_rollout(
        self,
        *,
        condition: str,
        policy: BasePolicy,
        source_snapshot: StateSnapshot,
        action_prefix: List[np.ndarray],
        seed: int,
        alternative_memory_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Set up environment and policy for an explicit or legacy recovery condition.
        
        Args:
            condition: Condition identifier (M_REPLAY_PRESERVED, M_INJECT_PRESERVED,
                       M_INJECT_RESET, M_INJECT_ALTERNATIVE, or legacy B0-B4).
            policy: Policy architecture being evaluated.
            source_snapshot: Target physical state snapshot.
            action_prefix: Recorded sequence of pre-failure Cartesian actions.
            seed: Environment initialization seed.
            alternative_memory_state: Optional donor/alternative memory state for M_INJECT_ALTERNATIVE.
            
        Returns:
            setup_info: Metadata dictionary containing validation status, memory state, and configuration.
        """
        cond_upper = condition.upper()

        # =====================================================================
        # 1. Condition A: Replay with Preserved Policy Memory
        # =====================================================================
        if cond_upper in [COND_REPLAY_PRESERVED, "REPLAY_PRESERVED", "B0"]:
            # Replay full prefix through environment and policy
            obs, info = self.env.reset(seed=seed)
            policy.reset_memory(obs)

            for act in action_prefix:
                policy.act(obs, deterministic=True)
                obs, r, term, trunc, info = self.env.step(act)

            current_snap = self.env.get_state_snapshot()
            state_error = float(np.linalg.norm(current_snap.qpos - source_snapshot.qpos))

            h_norm = 0.0
            h = policy.get_hidden_state()
            if h is not None and isinstance(h, torch.Tensor):
                h_norm = float(torch.norm(h).item())

            return {
                "condition": COND_REPLAY_PRESERVED if "M_" in cond_upper or "REPLAY" in cond_upper else "B0",
                "canonical_memory_condition": COND_REPLAY_PRESERVED,
                "execution_mode": "replay",
                "state_matching_error": state_error,
                "obs_history_status": "preserved",
                "action_history_status": "preserved",
                "hidden_state_status": "preserved",
                "initial_hidden_norm": h_norm,
                "remaining_horizon": self.env.remaining_horizon,
                "current_observation": obs,
                "validation_status": "validated",
            }

        # =====================================================================
        # 2. Condition B: Matched Injection with Preserved Policy Memory
        # =====================================================================
        elif cond_upper in [COND_INJECT_PRESERVED, "INJECT_PRESERVED"]:
            # Extract preserved policy memory from prefix unrolling
            preserved_mem = self.unroll_policy_memory_on_prefix(policy, seed, action_prefix)

            # Inject candidate matched snapshot into environment without env prefix replay
            injected_obs = self.env.inject_matched_state(source_snapshot, preserve_horizon=True)
            current_snap = self.env.get_state_snapshot()
            state_error = float(np.linalg.norm(current_snap.qpos - source_snapshot.qpos))

            # Restore preserved memory into policy
            policy.set_memory_state(preserved_mem)

            h_norm = 0.0
            h = policy.get_hidden_state()
            if h is not None and isinstance(h, torch.Tensor):
                h_norm = float(torch.norm(h).item())

            return {
                "condition": COND_INJECT_PRESERVED,
                "canonical_memory_condition": COND_INJECT_PRESERVED,
                "execution_mode": "injection",
                "state_matching_error": state_error,
                "obs_history_status": "preserved",
                "action_history_status": "preserved",
                "hidden_state_status": "preserved",
                "initial_hidden_norm": h_norm,
                "remaining_horizon": self.env.remaining_horizon,
                "current_observation": injected_obs,
                "validation_status": "validated",
            }

        # =====================================================================
        # 3. Condition C: Matched Injection with Reset Policy Memory
        # =====================================================================
        elif cond_upper in [COND_INJECT_RESET, "INJECT_RESET", "B4"]:
            # Directly inject candidate matched snapshot into environment
            injected_obs = self.env.inject_matched_state(source_snapshot, preserve_horizon=True)
            current_snap = self.env.get_state_snapshot()
            state_error = float(np.linalg.norm(current_snap.qpos - source_snapshot.qpos))

            # Explicitly reset policy memory
            policy.reset_memory(injected_obs)
            if hasattr(policy, "ablate_history"):
                policy.ablate_history(injected_obs, ablate_obs=True, ablate_act=True)

            h_norm = 0.0
            h = policy.get_hidden_state()
            if h is not None and isinstance(h, torch.Tensor):
                h_norm = float(torch.norm(h).item())

            return {
                "condition": COND_INJECT_RESET if "M_" in cond_upper or "RESET" in cond_upper else "B4",
                "canonical_memory_condition": COND_INJECT_RESET,
                "execution_mode": "injection",
                "state_matching_error": state_error,
                "obs_history_status": "ablated" if cond_upper == "B4" else "reset",
                "action_history_status": "ablated" if cond_upper == "B4" else "reset",
                "hidden_state_status": "reset",
                "initial_hidden_norm": h_norm,
                "remaining_horizon": self.env.remaining_horizon,
                "current_observation": injected_obs,
                "validation_status": "validated",
            }

        # =====================================================================
        # 4. Condition D: Matched Injection with Alternative Compatible Memory
        # =====================================================================
        elif cond_upper in [COND_INJECT_ALTERNATIVE, "INJECT_ALTERNATIVE"]:
            # Determine alternative compatible memory
            if alternative_memory_state is not None:
                alt_mem = copy.deepcopy(alternative_memory_state)
            else:
                # Construct deterministic alternative memory by unrolling prefix then inverting/shuffling
                nominal_mem = self.unroll_policy_memory_on_prefix(policy, seed, action_prefix)
                alt_mem = copy.deepcopy(nominal_mem)
                if alt_mem.get("hidden_state") is not None and isinstance(alt_mem["hidden_state"], torch.Tensor):
                    # Invert hidden state: creates a bounded, valid, but geometrically opposing belief vector
                    alt_mem["hidden_state"] = -alt_mem["hidden_state"].detach().clone()
                if "obs_buffer" in alt_mem and len(alt_mem["obs_buffer"]) > 1:
                    alt_mem["obs_buffer"] = list(reversed(alt_mem["obs_buffer"]))

            # Directly inject matched state into environment
            injected_obs = self.env.inject_matched_state(source_snapshot, preserve_horizon=True)
            current_snap = self.env.get_state_snapshot()
            state_error = float(np.linalg.norm(current_snap.qpos - source_snapshot.qpos))

            # Load alternative memory into policy
            policy.set_memory_state(alt_mem)

            h_norm = 0.0
            h = policy.get_hidden_state()
            if h is not None and isinstance(h, torch.Tensor):
                h_norm = float(torch.norm(h).item())

            return {
                "condition": COND_INJECT_ALTERNATIVE,
                "canonical_memory_condition": COND_INJECT_ALTERNATIVE,
                "execution_mode": "injection",
                "state_matching_error": state_error,
                "obs_history_status": "alternative",
                "action_history_status": "alternative",
                "hidden_state_status": "alternative",
                "initial_hidden_norm": h_norm,
                "remaining_horizon": self.env.remaining_horizon,
                "current_observation": injected_obs,
                "validation_status": "validated",
            }

        # =====================================================================
        # Legacy Intermediate Ablation Conditions (B1, B2, B3)
        # =====================================================================
        elif cond_upper in ["B1", "B2", "B3"]:
            # Bring policy to t_fail state by unrolling prefix
            obs, info = self.env.reset(seed=seed)
            policy.reset_memory(obs)
            for act in action_prefix:
                policy.act(obs, deterministic=True)
                obs, r, term, trunc, info = self.env.step(act)

            injected_obs = self.env.inject_matched_state(source_snapshot, preserve_horizon=True)
            current_snap = self.env.get_state_snapshot()
            state_error = float(np.linalg.norm(current_snap.qpos - source_snapshot.qpos))

            if cond_upper == "B1":
                if hasattr(policy, "ablate_history"):
                    policy.ablate_history(injected_obs, ablate_act=True)
                hidden_status = "preserved"
            elif cond_upper == "B2":
                if hasattr(policy, "ablate_history"):
                    policy.ablate_history(injected_obs, ablate_obs=True)
                hidden_status = "preserved"
            else:  # B3
                policy.reset_hidden_state()
                hidden_status = "reset"

            h_norm = 0.0
            h = policy.get_hidden_state()
            if h is not None and isinstance(h, torch.Tensor):
                h_norm = float(torch.norm(h).item())

            return {
                "condition": cond_upper,
                "canonical_memory_condition": cond_upper,
                "execution_mode": "injection",
                "state_matching_error": state_error,
                "obs_history_status": "ablated" if cond_upper == "B2" else "preserved",
                "action_history_status": "ablated" if cond_upper == "B1" else "preserved",
                "hidden_state_status": hidden_status,
                "initial_hidden_norm": h_norm,
                "remaining_horizon": self.env.remaining_horizon,
                "current_observation": injected_obs,
                "validation_status": "validated",
            }

        else:
            raise ValueError(f"Unknown condition: {condition}")
