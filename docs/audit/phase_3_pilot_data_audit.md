# Phase 3 Pilot Data Audit

> **Audit Target:** Existing Pilot Outputs (`results/pilot_recovery/`, `results/training_logs/`, `notebooks/`, `figures/`)  
> **Evaluation Date:** 2026-11-09  
> **Audit Status:** `Verified & Audited`  
> **Methodological Rule:** Strict data preservation — original pilot data files remain completely unmodified.

---

## 1. Inventory of Audited Pilot Artifacts

The existing pilot data repository contains the following artifacts:

| Directory / Artifact Path | File Count / Size | Content Description | Provenance & Integrity Status |
|---|---|---|---|
| `results/pilot_recovery/rollout_manifest.json` | 1 file (1.2 KB) | High-level execution manifest for 40 pilot episodes | `Verified` (Deterministic config, seed 42) |
| `results/pilot_recovery/rollout_metrics.json` | 1 file (6.8 KB) | Nominal, deviation, and recovery metrics across MLP & GRU | `Verified` (Exact numerical records) |
| `results/pilot_recovery/condition_report.json` | 1 file (4.1 KB) | Detailed scenario-level B0/B2/B4 counterfactual outcomes | `Verified` (Coincides with metrics) |
| `results/pilot_recovery/matching_report.json` | 1 file (12.4 KB) | 45 pairwise matching distance evaluations and rejections | `Verified` (Component breakdown present) |
| `results/pilot_recovery/episodes/reactive_mlp/nominal/` | 20 JSON + 20 NPZ | Individual episode logs (seeds `42 + i*7`, i=0..19) | `Verified` (Full trajectory arrays) |
| `results/pilot_recovery/episodes/history_gru/nominal/` | 20 JSON + 20 NPZ | Individual episode logs (seeds `42 + i*7`, i=0..19) | `Verified` (Full trajectory arrays) |
| `results/training_logs/reactive_mlp_training_log.json` | 1 file (1.8 KB) | 25-epoch behavioral cloning training/val loss history | `Verified` (Val MSE: $4.01 \times 10^{-6}$) |
| `results/training_logs/history_gru_training_log.json` | 1 file (1.8 KB) | 25-epoch behavioral cloning training/val loss history | `Verified` (Val MSE: $4.04 \times 10^{-6}$) |
| `notebooks/01..04_*.ipynb` | 4 notebooks | Executed Jupyter analysis notebooks with cell outputs | `Verified` (Outputs rendered) |
| `figures/paper/` & `figures/exploratory/` | 14 PNG + 14 PDF | 7 diagnostic figures at 600 DPI + vector PDF | `Verified` (Manifest checksums match) |

---

## 2. Comprehensive Episode-by-Episode and Condition Audit

### 2.1 Nominal Rollout Episodes ($N = 40$)
- **Reactive MLP Nominal ($N=20$, Seeds 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175):**
  - **Successes ($R=1$):** 4 episodes (seeds 42, 56, 119, 147).
  - **Failures ($R=0$):** 16 episodes.
  - **Trajectory Archives:** All 20 NPZ files present; shapes $(T, 20)$ for observations, $(T, 3)$ for actions, $(T, 19)$ for physical states.
  - **Metadata Integrity:** Full SHA-256 environment and policy config hashes present.
- **History-Aware GRU Nominal ($N=20$, Seeds 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175):**
  - **Successes ($R=1$):** 6 episodes (seeds 42, 56, 77, 119, 147, 161).
  - **Failures ($R=0$):** 14 episodes.
  - **Trajectory Archives:** All 20 NPZ files present; consistent array shapes.

### 2.2 Induced Deviation & Admitted Counterfactual Recovery Scenarios ($N = 8$)

The Privileged Oracle Filter audited all 40 candidate deviation episodes ($20$ MLP + $20$ GRU) and admitted exactly 8 recoverable scenarios:

| Scenario UID | Policy ID | Seed | $t_d$ | Failure Type | Deviation Yaw ($\Delta \theta$) | Lateral Drift ($\Delta y$) | Oracle Recovery ($R_{\text{oracle}}$) | B0 Outcome | B2 Outcome | B4 Outcome | Matched State Error | Remaining Horizon ($T - t_d$) | Safety Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `scen_mlp_s70_t44` | `reactive_mlp` | 70 | 44 | Off-center slip | $26.4^\circ$ | $2.1\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 106 | Pass ($\le 50$ N) |
| `scen_mlp_s112_t57` | `reactive_mlp` | 112 | 57 | Off-center slip | $27.1^\circ$ | $2.0\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 93 | Pass ($\le 50$ N) |
| `scen_mlp_s119_t83` | `reactive_mlp` | 119 | 83 | Off-center slip | $25.9^\circ$ | $2.0\text{ cm}$ | $1$ (Admitted) | $1$ (Success) | $1$ (Success) | $1$ (Success) | $0.0$ | 67 | Pass ($\le 50$ N) |
| `scen_mlp_s126_t47` | `reactive_mlp` | 126 | 47 | Off-center slip | $28.3^\circ$ | $2.2\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 103 | Pass ($\le 50$ N) |
| `scen_mlp_s154_t57` | `reactive_mlp` | 154 | 57 | Off-center slip | $26.8^\circ$ | $2.1\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 93 | Pass ($\le 50$ N) |
| `scen_gru_s77_t87` | `history_gru` | 77 | 87 | Off-center slip | $24.8^\circ$ | $2.0\text{ cm}$ | $1$ (Admitted) | $1$ (Success) | $1$ (Success) | $1$ (Success) | $0.0$ | 63 | Pass ($\le 50$ N) |
| `scen_gru_s126_t44` | `history_gru` | 126 | 44 | Off-center slip | $25.2^\circ$ | $2.1\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 106 | Pass ($\le 50$ N) |
| `scen_gru_s168_t66` | `history_gru` | 168 | 66 | Off-center slip | $24.1^\circ$ | $2.0\text{ cm}$ | $1$ (Admitted) | $0$ (Fail) | $0$ (Fail) | $0$ (Fail) | $0.0$ | 84 | Pass ($\le 50$ N) |

---

## 3. Discrepancy & Gap Identification

1. **Storage Discrepancy (Logged vs Aggregated):**
   - *Observation:* While all 40 nominal episodes were fully serialized as individual JSON metadata and NPZ trajectory archives under `results/pilot_recovery/episodes/<policy>/nominal/`, the 40 induced deviation rollouts and their associated B0/B2/B4 counterfactual rollouts were saved in summary JSON form (`results/pilot_recovery/condition_report.json` and `rollout_metrics.json`), rather than having individual per-episode subdirectories (`episodes/<policy>/induced_deviation/` and `episodes/<policy>/B0/`, `B2/`, `B4/`).
   - *Severity:* Low for pilot purposes (all condition metrics, deviation times, yaw angles, drift magnitudes, and success flags are preserved in JSON reports), but Phase 5 must mandate full per-condition NPZ serialization for every counterfactual rollout.
2. **Missing Longitudinal Diagnosis State Labels:**
   - *Observation:* The metrics currently record binary detection ($t_d$), physical deviation magnitude, and final task success ($R$), but do not record intermediate classification tags for explicit fault diagnosis (e.g. distinguishing slip vs stall) or corrective phase duration.
3. **No Duplicate or Inconsistent Episodes Found:**
   - All 20 random seeds (`42, 49, ..., 175`) are unique, strictly monotonically ordered, and reproducible.
4. **State Matching Precision Confirmed:**
   - All 8 counterfactual matched state injections recorded a state matching error of exactly $0.0$, confirming bitwise-lossless state restoration across all generalized coordinates.

