# Phase 0.5 Correction Audit Report

> **Audit Date:** 2026-11-06  
> **Auditor:** Lead Robotics Researcher, Systems Architect & Reproducibility Auditor  
> **Status:** AUDIT COMPLETE — RESEARCH FREEZE ENFORCED  
> **Mandate:** Phase 1 remains strictly paused pending explicit user approval.

---

## 1. Corrected Novelty Status & Language Discipline

- **Updated Status:** **PROVISIONALLY PROMISING — DIRECT OVERLAP REQUIRES DETAILED COMPARISON**.
- **Claims Correction:** All premature assertions of "PASSED & VERIFIED" or "No published benchmark performs this protocol" have been replaced across the documentation.
- **Formal Decision Classification:** **NOVELTY SUPPORTED** (with rigorous boundary positioning), documented in [`docs/literature/novelty_go_no_go_decision.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/literature/novelty_go_no_go_decision.md).

---

## 2. Direct Overlap Findings Across 5 Related Papers

Detailed 13-dimension comparison documented in [`docs/literature/direct_overlap_analysis.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/literature/direct_overlap_analysis.md):

1. **Counterfactual Auditing of History-Conditioned Robot Policies (CMA, arXiv:2609.27247):**
   - *Overlap:* Explores counterfactual history manipulation and memory auditing.
   - *Key Distinction:* CMA evaluates *nominal task instruction memory* (e.g. remembering object placement cues across reconverging trajectories). It does **not** evaluate physical execution failures, contact slips, collisions, failure detection, failure diagnosis, or recovery success metrics ($H_R$).
2. **Causal-History Test-Time Scaling for Failure Recovery in Autoregressive WAMs (FARE, arXiv:2609):**
   - *Overlap:* Investigates causal history in the context of robot recovery.
   - *Key Distinction:* FARE is an *algorithmic test-time inference method* that manipulates the autoregressive KV cache of World-Action Models to prevent prediction drift on the robot. It is **not** a benchmark evaluation protocol that audits policy evaluation validity across model families under matched physical state injections.
3. **RoboRecover (arXiv:2409.28952):**
   - *Overlap:* Reconstructs intermediate deviation states using action-prefix replay (Condition B).
   - *Key Distinction:* RoboRecover evaluates recovery *only* from replayed prefixes. It **never** performs matched-state counterfactual injection without history (Condition C), nor does it compute history-dependence metrics $H_R = R_{\text{replay}} - R_{\text{injected}}$, nor does it decompose recovery into detection vs. diagnosis vs. correction.
4. **LIBERO-Recover:**
   - *Overlap:* Failure recovery benchmarks across 4 recovery tiers.
   - *Key Distinction:* Focuses on static initial scenes per tier; does not match physical states across differing causal execution histories.
5. **LIBERO-Pro / LIBERO-Pro2.0:**
   - *Overlap:* 22 static and 20 runtime perturbation evaluations.
   - *Key Distinction:* Tests robustness degradation under runtime disturbances; does not isolate causal action history from instantaneous physical state configurations.

---

## 3. Corrected History Definition & Intervention Specification

Detailed in [`docs/methodology/history_intervention_specification.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/history_intervention_specification.md), "history" is formally decomposed into 11 distinct streams:
1. Physical simulator state ($s_t = [q, \dot{q}, \text{act}, \text{warmstart}]$)
2. Observation history ($H_t^o = (o_0, \dots, o_t)$)
3. Action history ($H_t^a = (a_0, \dots, a_{t-1})$)
4. Proprioceptive history ($H_t^{\text{prop}}$)
5. Visual history ($H_t^{\text{vis}}$)
6. Contact history ($H_t^c$)
7. Reward & Progress history ($H_t^r, H_t^g$)
8. Policy hidden state ($h_t^{\pi}$)
9. Random-number generator state ($\xi_t$)
10. Failure-detection history ($H_t^{\text{diag}}$)

---

## 4. Corrected Evaluation Condition Definitions & Equivalence Analysis

Detailed in [`docs/methodology/minimum_viable_experiment.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/minimum_viable_experiment.md):
- **Condition A (Natural Execution) vs. Condition B (Prefix Replay):**
  - Under deterministic physics and deterministic policy execution, **Condition A and Condition B are structurally identical** ($s_A(t_d) \equiv s_B(t_d)$).
  - Condition A is retained strictly as an **ecological fidelity baseline** to verify that replaying the prefix produces zero state drift. It is **not** treated as an independent causal condition unless stochastic noise models or non-deterministic dynamics are introduced.
- **The Primary Causal Comparison:**
  - Formally established as **Condition B (Preserved History)** versus **Condition C (Matched State Injection without History)**:
    $$H_R = R(\text{Condition B}) - R(\text{Condition C})$$

---

## 5. Environment-Check Status & Failure Investigation

Detailed in [`docs/audit/environment_status.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/audit/environment_status.md):
- **Conda Investigation:** `conda --version` exited with code 1 because Anaconda/Miniconda is not in the system user PATH. Python 3.11.0 is installed directly in the user profile with all core scientific dependencies present. Conda is not required.
- **MuJoCo XML Draft Investigation:** An unprompted draft XML file lacked explicit mass on intermediate links (`ValueError: mass and inertia`). The draft file and directory were completely removed.
- **Verified Installed & Unit-Tested Dependencies:**
  - Python 3.11.0 (Exit code 0)
  - NumPy 2.4.6, SciPy 1.17.1, Pandas 2.3.3, Scikit-learn 1.8.0, PyYAML 6.0.3, Pydantic 2.13.4 (All importable, Exit code 0)
  - PyTorch 2.13.0+cpu (Tensor operations verified, Exit code 0)
  - Gymnasium 1.3.0 (`Pusher-v5` initialized, Exit code 0)
  - MuJoCo 3.10.0 (Simulation step executed, Exit code 0)
  - Pytest 9.1.1 (2 tests passed in 0.13s, Exit code 0)

---

## 6. Task Availability & Verification

Detailed in [`docs/methodology/task_availability.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/methodology/task_availability.md):
- The planning identifier `Push-to-Target-v0` was an **invented planning placeholder**. It is **not** an existing installed environment.
- The reference has been renamed across all configs and documentation to:
  `planned_custom_push_target_env`
- Status: **Planned Custom Environment (Scheduled for Phase 1)**.
- Fallback Baseline: Standard `Pusher-v5` in Gymnasium is installed and verified if custom MJCF development encounters unexpected obstacles.

---

## 7. Statistical Plan Status (Provisional)

Detailed in [`docs/statistics/provisional_analysis_plan.md`](file:///D:/PROJECT/CASUAL%20HISTORY%20IN%20ROBOT%20POLICY%20RECOVERY/causal-history-recovery/docs/statistics/provisional_analysis_plan.md):
- The 5-seed plan and 50–100 episode estimates are explicitly marked as **provisional**.
- Statistical tests (Wilcoxon vs. McNemar's paired test vs. GLMM) will be selected based on empirical pilot data.
- Pilot rollouts in Phase 7 must estimate matching yield rate ($\eta_{\text{match}}$), oracle recoverability ($\eta_{\text{recoverable}}$), and outcome variance before official benchmark runs.

---

## 8. Remaining Blockers
- **None.** Codebase is clean, dependencies are verified, and research boundaries are fully clarified.

---

## 9. Whether Phase 1 is Recommended
- Phase 1 is technically prepared and well-bounded. However, per the Phase Gate Protocol:

> **“Phase 1 remains paused pending explicit user approval.”**

