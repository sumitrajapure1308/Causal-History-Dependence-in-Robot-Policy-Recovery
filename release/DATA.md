# Data Management & Provenance Specification

## Primary Benchmark Data
- **Location:** `results/phase_12_stage_c/rollouts/rollout_records.jsonl`
- **Volume:** Exactly 20,000 JSONL records ($15.5\text{ MB}$).
- **Structure:** Balanced $2 \times 2 \times 4 \times 5 \times 5 \times 50$ factorial design.
  - Tasks (2): `task1_cube`, `task2_puck`
  - Failure Modes (2): `rotational_slip`, `contact_loss`
  - Policies (4): `reactive_mlp`, `history_gru`, `recovery_augmented_mlp`, `recovery_augmented_gru`
  - Conditions (5): $B_0, B_1, B_2, B_3, B_4$
  - Replicate Seeds (5): `15001, 15002, 15003, 15004, 15005`
  - Scenarios (200): 50 per cell (Disjoint seeds $\ge 10000$)

## Scenario Manifest
- **Location:** `results/phase_12_stage_c/scenario_manifest.json`
- **Contents:** Exact failure snapshots, yaw deviations, lateral drifts, and privileged oracle recoverability audit.

## Data Lineage & Immutability Rules
Raw rollout data (`results/phase_12_stage_c/rollouts/`) is strictly immutable. All analysis scripts read directly from these JSONL records without altering source data.
