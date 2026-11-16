# Final Archival Submission Decision

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/final_decision/final_submission_decision.md`  
**Milestone:** Phase 23 — Final Submission Decision and Journal-Readiness Gate  
**Date:** 2026-11-10  
**Verification Status:** `Final submission decision` | `Submission decision` | `Go/No-Go decision` | `Verified`  

---

## 1. Formal Submission Decision

> ### **“GO — submission-ready with documented limitations.”**

---

## 2. Decision Parameters & Venue Governance

- **Primary Target Venue:** **NeurIPS Track on Datasets and Benchmarks**
  - Track Profile: Archival venue for rigorous evaluation protocols, negative control validation, and reproducible benchmark releases in machine learning and robotics.
- **Secondary Target Venues:**
  - **Alternative A:** **Robotics: Science and Systems (RSS)** — Robotics algorithm, benchmark, and systems focus.
  - **Alternative B:** **IEEE Robotics and Automation Letters (RA-L)** — Rapid letter track with concise 6-to-8 page presentation.
- **Submission Type:** Archival Benchmark and Evaluation Track Research Paper (Double-Blind).
- **Submission Deadline:** Official Track Deadline (Annual Cycle: Round 1 June / Round 2 September).
- **Required Actions:**
  1. Freeze all on-disk artifacts, code checkpoints, dataset manifests, and cryptographic ledgers.
  2. Enforce Phase Gate Protocol: maintain strict submission pause until explicit user instruction is issued.
  3. Compile double-blind LaTeX manuscript using official `neurips_2026.sty` template upon authorization.
  4. Perform pre-flight cryptographic digest verification against `final_submission_manifest.md`.
  5. Ingest submission bundle into OpenReview portal $\ge 24$ hours prior to deadline cutoff.
- **Owner:** Lead Author / Autonomous Agent System
- **Deadline:** Day 0 (Packaging freeze), Target Submission Date (Portal upload)
- **Status:** **GO — submission-ready with documented limitations; portal transmission paused pending explicit user approval.**
- **Risk Assessment:** Low operational risk. Reviewer queries regarding simulation scope and null recovery effects are thoroughly addressed by pre-registered negative controls, physical contact force analyses, and pre-structured rebuttal templates.
- **Mitigation:** Empirical grounding in 20,000 Stage C rollouts, negative control zero-discordance validation (0/200 pairs, $[0.00\%, 1.83\%]$ CI), and contact normal force attenuation ($d=3.99$, $p < 10^{-15}$).
- **Required Artifacts:**
  - 9-page compiled double-blind manuscript PDF.
  - Supplementary materials PDF (Appendices S1–S13).
  - Standalone release package ZIP (`anonymous_release_staging.zip`, 16,393 bytes, 23 files).
  - Benchmark scenario definitions (200 matched scenarios) and evaluation summaries.
  - Cryptographic provenance manifests (`phase_22_file_hashes.json`, `phase_23_file_hashes.json`).
- **Required Approvals:** User approval gate (MANDATORY).
- **Required Checks:**
  - 67/67 unit and integration tests passing (`pytest tests -v` in under 15 seconds).
  - Release smoke test passing in under 3.5 seconds (`release/smoke_test.py`).
  - Sub-atomic state matching verification ($D \le 10^{-10}$ m).
  - Bitwise trajectory determinism ($D = 0.0$).
  - Negative control validation confirmed (0/200 discordant pairs).
- **Required Submissions:** Official OpenReview portal submission receipt.
- **Required Follow-Ups:** Post-submission integrity audit, reviewer discussion monitoring, and rebuttal dispatch.

---

## 3. Scope Bounding & Documented Limitations

1. **Simulation Scope:** All benchmarks and counterfactual interventions are executed in MuJoCo 3.10.0 rigid-body simulation. Physical Franka Panda hardware deployment is documented as future work.
2. **Task & Failure Scope:** Evaluations are bounded to 2 manipulation tasks (push-to-target, obstacle-avoidance push) under 2 execution failure modes (velocity pulse, end-effector slip).
3. **Decoupling Mechanism:** Policy action divergence in recurrent architectures ($\|\Delta a_0\| = 0.0038$ m/step, $d=3.99$) is physically damped by normal contact forces and surface friction before terminal goal reach ($p_\text{adj} \ge 0.2500$).
4. **Independent Project Boundary:** Complete conceptual, architectural, and operational separation from past projects (MIND-Contact / MIND-Contact++).
5. **No Universal Generalization:** History invariance is proven specifically for the evaluated policy suite and physical contact regimes; no universal claim of history invariance across all manipulation tasks is made.

---
*Decision codified and certified by Autonomous Agent System.*

