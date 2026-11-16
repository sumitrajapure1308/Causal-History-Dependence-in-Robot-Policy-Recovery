# Recovery Training Data Specification

> **Document Type:** Data Generation & Representation Specification  
> **Project Title:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
> **Phase:** 7 (Recovery-Augmented Policy Development)  
> **Date:** 2026-11-09  
> **Status:** `Verified`  
> **Anti-Contamination Rule:** Training data MUST be strictly partitioned from evaluation data. Zero overlap with frozen Phase 5/6 paired scenarios ($N=38$) or evaluation seeds (`[42, 500, 2000]`).

---

## 1. Motivation & Purpose

Phase 6 established that policies trained exclusively on nominal demonstration data suffer from **behavioral incapacity**: when off-manifold failures occur, they fail to execute corrective re-alignments and simply push open-loop forward.

To investigate whether causal history affects recovery performance, policies must possess basic **recovery maneuvering competence** (disengagement, re-alignment, and corrective pushing). This dataset provides behavioral demonstrations across both nominal and recovered trajectories.

---

## 2. Cohort Separation & Anti-Leakage Protocol

The dataset enforces strict partition boundaries:

```
Dataset Cohort Structure:
├── Training Cohort (Seeds 3000 – 3039):
│   ├── 20 Nominal Demonstrations (unperturbed pushing)
│   ├── 20 Recovery Demonstrations (perturbation + multi-phase recovery)
│   └── 10 Failed Recovery Demonstrations (severe/unrecoverable trajectories)
├── Validation Cohort (Seeds 3040 – 3049):
│   ├── 5 Nominal Demonstrations
│   └── 5 Recovery Demonstrations
├── Pilot Evaluation Cohort (Phase 3/4 Pilot, Seeds 42, 500, 2000, 10 episodes)
└── Benchmark Test Cohort (FROZEN 38 Paired Scenarios from Phase 5/6)
```

**Zero Contamination Guarantee:**
- Test scenarios use base seeds `42, 500, 2000`.
- Training demonstrations use seeds `3000` to `3049`.
- No benchmark scenario states or actions are present in the training set.

---

## 3. Data Representation & Feature Schema

Each sample in the dataset contains:

| Feature Name | Dimension | Type | Description |
|---|---|---|---|
| `obs_current` | 20 | `float32` | Standard low-dimensional observation from `PushTargetEnv` |
| `failure_detected` | 1 | `float32` | Causal slip detection signal ($1.0$ if $|yaw| > 15^\circ$ or $|y| > 2.5\text{ cm}$, else $0.0$) |
| `deviation_time` | 1 | `float32` | Normalized steps since deviation ($t_{\text{since}} / 100.0$) |
| `deviation_magnitude` | 1 | `float32` | Estimated yaw deflection magnitude in radians |
| `remaining_horizon` | 1 | `float32` | Normalized remaining steps ($T_{\text{rem}} / 150.0$) |
| `contact_present` | 1 | `float32` | Active contact indicator between pusher and cube ($1.0$ or $0.0$) |
| `action_history` | $10 \times 3$ | `float32` | Buffer of 10 previous action vectors |
| `obs_history` | $10 \times 24$ | `float32` | Buffer of 10 previous augmented observations |
| `target_action` | 3 | `float32` | Expert displacement delta $a_t \in [-0.02, 0.02]^3$ |
| `phase_label` | 1 | `int64` | Behavioral phase: 0 = nominal, 1 = retract, 2 = align, 3 = push |
| `recovery_success` | 1 | `int64` | Binary episode outcome ($1$ = completed with dwell, $0$ = failed) |

---

## 4. Multi-Phase Recovery Demonstration Trajectory

For recovery demonstrations, trajectories follow a three-phase closed-loop sequence:
1. **Phase 1: Disengagement & Retraction**
   - Retracts pusher away from the jammed/slipped cube ($a_x = -0.006\text{ m/step}$, 8 steps).
2. **Phase 2: Lateral Re-Alignment**
   - Maneuvers laterally to establish a standoff pose ($4.5\text{ cm}$ behind the rotated block along the ray to the goal).
3. **Phase 3: Directed Correction & Dwell**
   - Pushes through the center-of-mass towards the target zone ($r \le 0.06\text{ m}$), then halts inside the zone to satisfy 5 dwell steps.

---

## 5. Storage & Verification

- Output path: `data/processed/recovery_training_dataset.npz`
- Manifest: `data/processed/dataset_manifest.json`
- Dataset integrity verified via SHA-256 checksum and automated tensor validation.

