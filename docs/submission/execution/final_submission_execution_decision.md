# Final Submission Execution Decision

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/execution/final_submission_execution_decision.md`  
**Milestone:** Phase 20 — Final Submission Execution Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Submission decision` | `Go/No-Go decision` | `Submission execution package`  

---

## 1. Formal Execution Decision

> ### **“GO — submission-ready with documented limitations.”**

---

## 2. Decision Specifications & Submission Parameters

- **Primary Target Venue:** **NeurIPS Track on Datasets and Benchmarks**
- **Secondary Target Venues:** 
  - **Alternative A:** **Robotics: Science and Systems (RSS)**
  - **Alternative B:** **IEEE Robotics and Automation Letters (RA-L)**
- **Submission Type:** Archival Benchmark and Evaluation Track Research Paper
- **Submission Deadline:** Official Track Deadline (Annual Cycle: Round 1 June / Round 2 September)
- **Required Actions:**
  1. Freeze all on-disk benchmark artifacts, code, checkpoints, and cryptographic manifests.
  2. Maintain strict submission pause until explicit user approval is granted.
  3. Compile double-blind LaTeX manuscript using official `neurips_2026.sty` template.
  4. Perform pre-flight cryptographic digest verification against `submission_execution_manifest.md`.
  5. Ingest submission files into OpenReview portal $\ge 24$ hours prior to deadline.
- **Owner:** Lead Author / Autonomous Agent System
- **Deadline:** Day 0 (Packaging freeze), Target Submission Date (Portal upload)
- **Status:** **GO — submission-ready with documented limitations; portal transmission paused pending explicit user approval.**
- **Risk Assessment:** Low operational risk. Reviewer queries regarding simulation scope and null recovery effects are thoroughly addressed by pre-registered negative controls, physical contact force analyses, and pre-structured rebuttal templates.
- **Mitigation:** Empirical grounding in 20,000 Stage C rollouts, negative control zero-discordance validation (0/200 discordant pairs), and contact normal force attenuation ($d=3.99$, $p < 10^{-15}$).
- **Required Artifacts:**
  - 9-page compiled double-blind manuscript PDF.
  - Supplementary material PDF (Appendices S1–S13).
  - Standalone release package ZIP (Dockerfile, conda env, models, smoke test).
  - Benchmark scenario definitions (200 matched scenarios) and evaluation summaries.
  - Cryptographic provenance manifests (`phase_19_file_hashes.json`, `phase_20_file_hashes.json`).
- **Required Approvals:** User approval gate (MANDATORY).
- **Required Checks:**
  - 67/67 unit and integration tests passing (`pytest tests -v` passing in under 12 seconds).
  - Release smoke test passing in under 3.0 seconds (`release/smoke_test.py`).
  - Sub-atomic state matching verification ($D \le 10^{-10}$ m).
  - Bitwise trajectory determinism ($D = 0.0$).
  - Negative control validation confirmed (0/200 discordant pairs).
- **Required Submissions:** Official OpenReview portal submission receipt.
- **Required Follow-Ups:** Post-submission integrity audit, reviewer discussion monitoring, and rebuttal dispatch.

---

## 3. Scope Bounding & Documented Limitations

1. **Simulation-Based Scope:** All benchmarks and counterfactual interventions are executed in MuJoCo 3.10.0 rigid-body simulation. Physical Franka Panda hardware deployment is documented as future work.
2. **Task & Failure Scope:** Evaluations are bounded to 2 manipulation tasks (push-to-target, obstacle-avoidance push) under 2 execution failure modes (velocity pulse, end-effector slip).
3. **Decoupling Mechanism:** Policy action divergence in recurrent architectures ($\|\Delta a_0\| = 0.0038$ m/step, $d=3.99$) is physically damped by normal contact forces and surface friction before terminal goal reach ($p_\text{adj} \ge 0.2500$).
4. **Independent Project Boundary:** Complete conceptual, architectural, and operational separation from past projects (MIND-Contact / MIND-Contact++).

---
*Decision finalized and certified by Autonomous Agent System.*

