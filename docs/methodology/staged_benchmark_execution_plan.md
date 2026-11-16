# Staged Benchmark Execution Protocol (Stages A, B, and C)

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Phase:** 11 — Benchmark-Readiness Audit and Staged Pilot-Scale Confirmation  
**Document:** `docs/methodology/staged_benchmark_execution_plan.md`  
**Status:** COMPLETED & SCIENTIFICALLY VALIDATED  
**Author:** Lead Robotics Researcher & Benchmark Architect  
**Date:** 2026-11-10  

---

## 1. Staged Execution Rationale

Running a 20,000-rollout benchmark in a monolithic, unverified run exposes the research to catastrophic pipeline errors, undetected serialization leaks, or silent metric bugs. To enforce rigorous scientific quality control, the benchmark execution is divided into three sequential, gated stages:

```
[Stage A: Small Confirmatory Smoke Run] (600 rollouts)
                    │
                    ▼  (Go/No-Go Gate 1: Pipeline & Log Verification)
[Stage B: Medium Confirmatory Pilot] (2,400 rollouts)
                    │
                    ▼  (Go/No-Go Gate 2: Power, Effect-Size, & Stability Check)
[Stage C: Full Official Benchmark] (20,000 rollouts — Phase 12+)
```

---

## 2. Stage Breakdown & Specification

### 2.1 Stage A: Small Confirmatory Smoke Run (Phase 11 Execution)
- **Objective:** Verify end-to-end operational pipeline health, scenario loading, condition semantics, log integrity, metric serialization, and runtime/storage budgets.
- **Matrix:**
  - Tasks: 2 (`PushTargetEnv`, `SecondPushTaskEnv`).
  - Failure Modes: 2 (Slip, Contact-Loss).
  - Scenarios per cell: 5 scenarios ($5 \times 2 \times 2 = 20\text{ total scenarios}$).
  - Policies: 4 (`reactive_mlp`, `history_gru`, `rec_aug_mlp`, `rec_aug_gru`).
  - Conditions: 5 (B0, B1, B2, B3, B4).
  - Evaluation Seeds: 3 (`9001, 9002, 9003`).
- **Total Rollouts:** $20\text{ scenarios} \times 4\text{ policies} \times 5\text{ conditions} \times 3\text{ seeds} = \mathbf{600\text{ rollouts}}$.
- **Go/No-Go Gate 1 Criteria:**
  1. 100% rollout completion (0 crash or timeout exceptions).
  2. Complete log manifest and artifact generation.
  3. Average runtime per rollout $\le 0.50\text{ seconds}$.
  4. Compact JSONL storage $\le 500\text{ bytes/rollout}$.
  5. Negative control invariance verified ($\Delta a = 0$ for `reactive_mlp`).

### 2.2 Stage B: Medium Confirmatory Pilot (Phase 11 Execution)
- **Objective:** Quantify empirical discordance rates, continuous trajectory effect sizes, variance estimates, and ranking stability across a statistically meaningful medium cohort.
- **Matrix:**
  - Tasks: 2 (`PushTargetEnv`, `SecondPushTaskEnv`).
  - Failure Modes: 2 (Slip, Contact-Loss).
  - Scenarios per cell: 20 scenarios ($20 \times 2 \times 2 = 80\text{ total scenarios}$).
  - Policies: 4 (`reactive_mlp`, `history_gru`, `rec_aug_mlp`, `rec_aug_gru`).
  - Conditions: 5 (B0, B1, B2, B3, B4).
  - Evaluation Seeds: 3 (`9001, 9002, 9003`).
- **Total Rollouts:** $80\text{ scenarios} \times 4\text{ policies} \times 5\text{ conditions} \times 3\text{ seeds} = \mathbf{2,400\text{ rollouts}}$.
- **Go/No-Go Gate 2 Criteria:**
  1. Zero safety violations ($0.0\%$).
  2. Policy ranking correlation Kendall's $\tau \ge 0.80$ (demonstrating ordinal stability).
  3. Trajectory divergence reliably detected in `rec_aug_gru`.
  4. Exact physical state matching error $D \le 1.0 \times 10^{-10}$.

### 2.3 Stage C: Full Confirmatory Benchmark (PAUSED — Phase 12+)
- **Objective:** Execute full-scale pre-registered hypothesis tests for Tier 1 (Binary Success) and Tier 2 (Continuous Error).
- **Matrix:**
  - Scenarios per cell: 50 scenarios ($50 \times 2 \times 2 = 200\text{ total scenarios}$).
  - Evaluation Seeds: 5 (`7001..7005`).
  - Policies: 4.
  - Conditions: 5.
- **Total Rollouts:** $200 \times 4 \times 5 \times 5 = \mathbf{20,000\text{ rollouts}}$.
- **Execution Rule:** Stage C will **NOT** be executed in Phase 11. It remains paused pending explicit user approval.

