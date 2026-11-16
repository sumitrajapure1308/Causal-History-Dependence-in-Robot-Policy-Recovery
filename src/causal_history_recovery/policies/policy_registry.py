"""Policy Registry and Factory.

Provides centralized registration and loading for policy architectures.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Type
import torch

from causal_history_recovery.policies.base_policy import BasePolicy
from causal_history_recovery.policies.reactive_mlp import ReactiveMLPPolicy
from causal_history_recovery.policies.history_gru import HistoryGRUPolicy
from causal_history_recovery.policies.recovery_augmented_mlp import RecoveryAugmentedMLPPolicy
from causal_history_recovery.policies.recovery_augmented_gru import RecoveryAugmentedGRUPolicy

_POLICY_REGISTRY: Dict[str, Type[BasePolicy]] = {
    "reactive_mlp": ReactiveMLPPolicy,
    "history_gru": HistoryGRUPolicy,
    "recovery_augmented_mlp": RecoveryAugmentedMLPPolicy,
    "recovery_augmented_gru": RecoveryAugmentedGRUPolicy,
}


def register_policy(name: str, policy_cls: Type[BasePolicy]) -> None:
    """Register a custom policy class."""
    _POLICY_REGISTRY[name.lower()] = policy_cls


def get_policy_class(name: str) -> Type[BasePolicy]:
    """Retrieve policy class by name."""
    name_clean = name.lower()
    if name_clean not in _POLICY_REGISTRY:
        raise KeyError(
            f"Policy '{name}' is not registered. Available policies: {list(_POLICY_REGISTRY.keys())}"
        )
    return _POLICY_REGISTRY[name_clean]


def create_policy(policy_type: str, config: Dict[str, Any]) -> BasePolicy:
    """Instantiate a policy from configuration dictionary."""
    policy_cls = get_policy_class(policy_type)
    return policy_cls(config)


def load_policy(checkpoint_path: str, device: str = "cpu") -> BasePolicy:
    """Load policy from checkpoint file."""
    checkpoint = torch.load(checkpoint_path, map_location=device)
    policy_type = checkpoint.get("policy_type")
    if not policy_type or policy_type not in _POLICY_REGISTRY:
        raise ValueError(
            f"Invalid checkpoint at {checkpoint_path}: policy_type '{policy_type}' unrecognized."
        )

    config = checkpoint.get("config", {})
    config["device"] = device
    policy = create_policy(policy_type, config)
    policy.load(checkpoint_path)
    return policy


def list_registered_policies() -> List[str]:
    """Return list of all registered policy type names."""
    return sorted(list(_POLICY_REGISTRY.keys()))

