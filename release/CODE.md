# Codebase Architecture & Modular Organization

The source code is structured as an installable Python package under `src/causal_history_recovery/`:

```
src/causal_history_recovery/
├── environments/               # MuJoCo/Gymnasium simulation environments
│   ├── push_target_env.py      # Task 1: Cube pushing with Coulomb friction
│   ├── second_push_task_env.py # Task 2: Puck pushing with altered mass and friction
│   ├── state_snapshot.py       # Lossless bitwise state capture and restore
│   └── assets/                 # MuJoCo XML physical model definitions
├── policies/                   # Policy architectures and registry
│   ├── reactive_mlp.py         # 2-layer MLP baseline (negative control)
│   ├── history_gru.py          # 1-layer GRU baseline
│   ├── recovery_augmented_mlp.py # Recovery-trained MLP
│   ├── recovery_augmented_gru.py # Recovery-trained GRU
│   └── policy_registry.py      # Unified factory and checkpoint loader
├── controllers/
│   └── privileged_oracle.py    # State-feedback reachability verifier
├── counterfactuals/
│   └── paired_scenario_generator.py # Scenario mining and failure trigger
├── matching/
│   └── state_matcher.py        # Composite distance and verification
├── metrics/
│   ├── history_dependence.py   # History dependence calculation
│   └── outcome_hierarchy.py    # 4-tier outcome categorization
└── rollout/
    ├── episode_logger.py       # Structured JSONL logging
    └── rollout_collector.py    # Batch rollout runner
```
