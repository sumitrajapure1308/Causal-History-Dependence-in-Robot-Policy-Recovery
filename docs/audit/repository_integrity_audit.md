# Repository Integrity Audit

> **Document Type:** System Architecture & Repository Path Integrity Audit  
> **Project Title:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
> **Phase:** 7 (Repository Integrity Audit & Recovery-Capable Baseline Development)  
> **Date:** 2026-11-09  
> **Status:** `Verified`  
> **Mandatory Rule:** All project files, checkpoints, results, figures, notebooks, logs, configurations, and datasets must reside strictly within the project root. Zero files outside the project boundary permitted.

---

## 1. Project Root Verification

The project root was formally audited and verified:
- **Verified Absolute Project Root:**  
  `D:\PROJECT\CASUAL HISTORY IN ROBOT POLICY RECOVERY\causal-history-recovery`
- **Verification Status:** `Verified`
- **Enforcement Mechanism:** Dynamic project-relative path resolution (`os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))` or `repo_root` search) enforced across all scripts, notebooks, test suites, and configuration loaders.
- **Parent Directory Boundary:** The parent folder `D:\PROJECT\CASUAL HISTORY IN ROBOT POLICY RECOVERY` contains only top-level workspace governance files (`AGENTS.md`, `GEMINI.md`, `README.md`) and the project subtree `causal-history-recovery/`. Zero experiment code, results, checkpoints, or data reside in the parent directory or user profile directory.

---

## 2. Directory Tree Audit

All 11 mandatory top-level directories were verified to exist within `causal-history-recovery/`:

| Directory Name | Expected Project Path | Exists | File Count | Primary Function / Contents | Verification Status |
|---|---|---|---|---|---|
| `configs/` | `causal-history-recovery/configs/` | Yes | 11 | Environment, policy, scenario, and benchmark YAML configurations | `Verified` |
| `docs/` | `causal-history-recovery/docs/` | Yes | 49 | Methodology, audit reports, decision logs, literature analysis | `Verified` |
| `notebooks/` | `causal-history-recovery/notebooks/` | Yes | 20 | Executed Jupyter notebooks (01 through 20) with visible cell outputs | `Verified` |
| `results/` | `causal-history-recovery/results/` | Yes | 215 | Rollout logs, paired scenarios, summary metrics, statistical JSONs | `Verified` |
| `figures/` | `causal-history-recovery/figures/` | Yes | 79 | 600 DPI diagnostic figures (PNG & PDF) in `exploratory/` and `paper/` | `Verified` |
| `scripts/` | `causal-history-recovery/scripts/` | Yes | 17 | Standalone execution pipelines, training, data generation, figure scripts | `Verified` |
| `src/` | `causal-history-recovery/src/` | Yes | 65 | Core Python package (`causal_history_recovery`) modules | `Verified` |
| `tests/` | `causal-history-recovery/tests/` | Yes | 28 | Unit and integration test suites (49 passing pytest cases) | `Verified` |
| `models/` | `causal-history-recovery/models/` | Yes | 2 | Trained policy checkpoints (`reactive_mlp_best.pt`, `history_gru_best.pt`) | `Verified` |
| `logs/` | `causal-history-recovery/logs/` | Yes | 0 | Runtime execution logs directory (initialized for daemon/batch runs) | `Verified` |
| `data/` | `causal-history-recovery/data/` | Yes | 0 | Demonstration datasets and interim replay buffers directory | `Verified` |

---

## 3. Comprehensive Artifact Audit Table

| artifact_type | expected_project_path | current_path | inside_project_root | status | action_taken | reference_updated |
|---|---|---|---|---|---|---|
| **Source Code** | `src/causal_history_recovery/` | `causal-history-recovery/src/causal_history_recovery/` | Yes | `Verified` | Audited package tree; all submodules import cleanly | Yes |
| **Configs (Env)** | `configs/environments/` | `causal-history-recovery/configs/environments/` | Yes | `Verified` | PushTargetEnv physics parameters verified | Yes |
| **Configs (Policies)** | `configs/policies/` | `causal-history-recovery/configs/policies/` | Yes | `Verified` | Architecture specifications verified | Yes |
| **Configs (Scenarios)** | `configs/scenarios/` | `causal-history-recovery/configs/scenarios/` | Yes | `Verified` | Paired sampling config verified | Yes |
| **Documentation** | `docs/` | `causal-history-recovery/docs/` | Yes | `Verified` | 49 markdown documents audited; no broken internal links | Yes |
| **Notebooks (Phase 3)** | `notebooks/01-04` | `causal-history-recovery/notebooks/01-04` | Yes | `Verified` | Fully executed with embedded outputs | Yes |
| **Notebooks (Phase 4)** | `notebooks/05-10` | `causal-history-recovery/notebooks/05-10` | Yes | `Verified` | Fully executed with embedded outputs | Yes |
| **Notebooks (Phase 5)** | `notebooks/11-14` | `causal-history-recovery/notebooks/11-14` | Yes | `Verified` | Fully executed with embedded outputs | Yes |
| **Notebooks (Phase 6)** | `notebooks/15-20` | `causal-history-recovery/notebooks/15-20` | Yes | `Verified` | Fully executed with embedded outputs | Yes |
| **Results (Pilot Eval)** | `results/pilot_evaluation/` | `causal-history-recovery/results/pilot_evaluation/` | Yes | `Verified` | 1,140 rollout logs and paired statistical reports intact | Yes |
| **Results (Paired Scen)** | `results/paired_scenarios/` | `causal-history-recovery/results/paired_scenarios/` | Yes | `Verified` | 38 validated paired scenario folders intact | Yes |
| **Results (Training Logs)**| `results/training_logs/` | `causal-history-recovery/results/training_logs/` | Yes | `Verified` | Phase 3 training loss histories intact | Yes |
| **Figures (Phase 3)** | `figures/exploratory/fig01-07` | `causal-history-recovery/figures/exploratory/` | Yes | `Verified` | 600 DPI PNG and vector PDF verified | Yes |
| **Figures (Phase 5)** | `figures/exploratory/fig08-18` | `causal-history-recovery/figures/exploratory/` | Yes | `Verified` | 600 DPI PNG and vector PDF verified | Yes |
| **Figures (Phase 6)** | `figures/exploratory/fig19-32` | `causal-history-recovery/figures/exploratory/` | Yes | `Verified` | 600 DPI PNG and vector PDF verified | Yes |
| **Checkpoints** | `models/checkpoints/` | `causal-history-recovery/models/checkpoints/` | Yes | `Verified` | 2 PyTorch model state dicts verified (MLP, GRU) | Yes |
| **Test Suites** | `tests/` | `causal-history-recovery/tests/` | Yes | `Verified` | 49 passing pytest cases | Yes |
| **Temporary Files** | N/A | Clean | Yes | `Verified` | Zero dangling scratch files or uncommitted temp dumps | Yes |
| **Duplicate Files** | N/A | `figures/paper/` duplicates Phase 3 exploratory figures | Yes | `Verified` | Maintained for paper-asset modularity | Yes |
| **Files Outside Root** | N/A | None | Yes | `Verified` | Zero external files detected; 100% inside project boundary | Yes |

---

## 4. Path Discipline & Broken Reference Verification

- **Hardcoded Absolute Path Search:** Scanned all `.py`, `.yaml`, and `.json` files for machine-specific path strings (`C:\Users`, `/home/`, etc.). 0 hardcoded machine paths found.
- **Dynamic Path Construction:** All scripts and modules utilize `os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))` or dynamic search routines.
- **Data Lineage:** Raw evaluation records (`detailed_records.jsonl`) remain strictly separated from aggregated summaries (`evaluation_summary.json`, `paired_comparisons.json`).
- **Audit Verdict:** **100% PASS — REPOSITORY INTEGRITY FULLY VERIFIED.**

