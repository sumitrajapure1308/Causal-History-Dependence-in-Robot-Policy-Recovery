# Reproducibility & Scientific Verification Policy

This document establishes the mandatory standards for data management, logging, random seed control, and experimental verification in `causal-history-recovery`.

---

## 1. Core Principles

1. **Deterministic Reproducibility:** Every empirical table, metric, and figure in the paper must be deterministically reproducible from raw logged data and automated analysis scripts.
2. **Immutable Raw Data:** Raw trajectory data, action prefixes, and simulator snapshots placed in `data/raw/` and `results/raw/` are write-once and strictly immutable. Processed aggregations reside in `data/processed/` and `results/tables/`.
3. **No Fabricated Data or Shortcuts:** Zero tolerance for mocked data, hand-edited logs, or unexecuted experiments.
4. **Transparent Negative Results:** In accordance with the methodology document, whether the null hypothesis is rejected ($H1: R_{\text{replay}} \neq R_{\text{injected}}$) or accepted ($R_{\text{replay}} \approx R_{\text{injected}}$), both findings are scientifically valid and will be published transparently.

---

## 2. Seed Control & Randomization Policy

- **Fixed Seed Hierarchy:**
  - Seed sets must be explicitly defined in `configs/experiments/`.
  - For pilot experiments: minimum 3 seeds (e.g., `[42, 1337, 2026]`).
  - For primary benchmark evaluations: minimum 5 seeds (e.g., `[42, 1337, 2026, 777, 999]`).
- **Seed Coverage:** Each seed independently controls:
  - Policy weight initialization.
  - Training dataset shuffle order.
  - Environment object placement jitter (within task initial state bounds).
  - Deviation injection sampling.
  - Evaluation episode rollout order.

---

## 3. Standard Episode Log Schema

Every evaluation rollout must emit a structured JSON / NPZ log entry conforming to the following schema:

```json
{
  "run_id": "eval_exp01_20261106_190000",
  "task_id": "block_push_01",
  "scenario_id": "task01_seed03_ep017_dev02",
  "policy_id": "bc_reactive_v1",
  "seed": 42,
  "condition": "Condition_C_Matched_Injection",
  "failure_source": "policy_slip",
  "history_condition": "none",
  "deviation_time": 47,
  "deviation_type": "partial_slip",
  "deviation_magnitude": {
    "position_error_m": 0.012,
    "orientation_error_rad": 0.08,
    "slip_distance_m": 0.021
  },
  "initial_state_hash": "sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "recovery_state_hash": "sha256_ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
  "state_matching_error": 0.0038,
  "observation_history_length": 1,
  "detection_time": 49,
  "detected_failure": true,
  "diagnosis_label": "partial_slip",
  "diagnosis_correct": true,
  "recovery_start": 50,
  "recovery_action_type": "regrasp_realign",
  "recovery_success": true,
  "final_success": true,
  "completion_time": 112,
  "collision_count": 0,
  "constraint_violations": 0,
  "path_length": 0.482,
  "action_cost": 14.25,
  "episode_return": 1.0,
  "confidence_before_failure": 0.94,
  "confidence_after_failure": 0.32
}
```

---

## 4. Verification Gates Before Official Experiments

Before running full-scale benchmark evaluations, the pipeline must pass:
1. **Deterministic Replay Test:** Replaying an action prefix from $t=0$ to $t=t_d$ must yield state distance $d(s_{\text{orig}}, s_{\text{replay}}) < 10^{-7}$.
2. **State Serialization Round-Trip Test:** Saving state to disk/memory and restoring it must produce bitwise identical simulator dynamics on subsequent steps.
3. **Oracle Feasibility Check:** An oracle/privileged controller must achieve $100\%$ recovery success on all accepted failure scenarios, ensuring no impossible states are included in the denominator of recovery rates.
4. **State Distance Invariant Check:** Matched state pairs must strictly satisfy $d(s_1, s_2) \le \epsilon$. Any scenario failing the threshold is logged as rejected and excluded from recovery benchmarking.

