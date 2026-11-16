# Novelty & Scientific Gap Audit

> **Audit Date:** 2026-11-06  
> **Auditor:** Lead Robotics Researcher & Reproducibility Auditor  
> **Status:** PROVISIONALLY PROMISING — DIRECT OVERLAP REQUIRES DETAILED COMPARISON (Novelty Decision: NOVELTY SUPPORTED per Detailed Direct Audit)

---

## 1. Executive Summary

A critical requirement of Phase 0 is to audit recent robotics literature and determine whether the proposed research idea overlaps excessively with published benchmarks. Specifically, recent benchmarks have already tackled robot recovery from execution deviations:
- **RoboRecover (arXiv:2409.28952, Sept 2024 / 2026):** Replays action prefixes to reconstruct intermediate deviation states across 2,000 scenarios in LIBERO and RoboTwin.
- **LIBERO-Recover (2024):** Evaluates failure recovery across 4 progressive recovery tiers (retry, adaptation, object state recovery, environmental recovery).
- **LIBERO-Pro / LIBERO-Pro2.0 (2025–2026):** Evaluates 22 static and 20 runtime interventions across 6 dimensions.
- **Counterfactual Memory Audit (CMA, arXiv:2609.27247):** Audits history-conditioned memory guidance on nominal tasks via memory bank swapping at observation reconvergence.
- **FARE (Test-Time Scaling for Autoregressive WAMs, arXiv:2609):** Searches history configurations at inference time to mitigate model drift.

### Audit Verdict:
**PROVISIONALLY PROMISING — DIRECT OVERLAP REQUIRES DETAILED COMPARISON.** To our knowledge, based on an audit of RoboRecover, LIBERO-Recover, LIBERO-Pro2.0, CMA, and FARE, existing literature evaluates either:
1. Replayed execution deviation states (preserving the exact prefix, e.g. RoboRecover), OR
2. Injected perturbed states (without matching the physical state to a policy's own execution failure), OR
3. Memory bank swapping at reconverged states on nominal tasks (CMA), OR
4. Online history search for autoregressive WAM inference (FARE).

Existing benchmarks do not perform a controlled paired comparison holding the instantaneous physical failure state constant while counterfactually altering or removing the preceding causal history.

Therefore, the contribution of this project is **not** claimed as "the first robot recovery benchmark", but rather:
> **A causal-history validity audit for robot recovery evaluation protocols.**

---

## 2. Granular Audit Against Key Benchmark Dimensions

| Specific Capability | Present in RoboRecover? | Present in LIBERO-Recover? | Present in LIBERO-Pro2.0? | Present in Proposed Work? | Audit Conclusion |
|---|---|---|---|---|---|
| **Same-state / different-history comparison** | ❌ No | ❌ No | ❌ No | ✅ **Yes** | Completely absent from literature. Unique novelty anchor. |
| **Matched physical-state injection without prefix** | ❌ No | ❌ No | ❌ No | ✅ **Yes** | Key intervention to isolate causal history from state. |
| **History-dependence metric ($H_R, H_R^{\text{abs}}$)** | ❌ No | ❌ No | ❌ No | ✅ **Yes** | Novel metric quantifying causal history impact. |
| **Detection-vs-Diagnosis decomposition** | ❌ No | ❌ Partial (tiers only) | ❌ No | ✅ **Yes** | Formal probabilistic decomposition $P(D)P(Z\|D)\dots$ |
| **Policy-ranking stability across protocols** | ❌ No | ❌ No | ❌ No | ✅ **Yes** | Tests whether current benchmark rankings are valid. |
| **Privileged oracle recoverability filtering** | ❌ Trajectory filter | ❌ Heuristic | ❌ Human check | ✅ **Yes** | Strictly isolates policy failure from task impossibility. |

---

## 3. Novelty Risks & Defensive Positioning

### Risk 1: Reviewers claiming "RoboRecover already did execution deviations"
- **Mitigation:** Acknowledge RoboRecover explicitly in the abstract, introduction, and related work. State clearly that RoboRecover introduced replayed execution deviations (Condition B), but did not test whether recovery is driven by the state or the history. RoboRecover is used directly as an established baseline protocol in our comparison table.

### Risk 2: Reviewers claiming "LIBERO-Recover already benchmarked recovery"
- **Mitigation:** Emphasize that LIBERO-Recover taxonomizes recovery into task levels (retry vs. adaptation vs. object/environmental recovery), whereas our work is a *validity audit* testing the foundational assumption of state sufficiency.

### Risk 3: Reviewers claiming "Simulators do not capture real-world causality"
- **Mitigation:** Explicitly bound the claims to *simulator intervention causality*. Do not claim universal physical causality or sim-to-real invariance without hardware data. The scientific claim is about **benchmark validity and policy behavior under controlled interventions**.

### Risk 4: Treating impossible physical failures as policy recovery failures
- **Mitigation:** Every scenario admitted into the evaluation must pass a privileged oracle controller test ($R_{\text{oracle}} = 1.0$). If an oracle cannot complete the task from that state, it is mathematically or physically unrecoverable and is filtered out before computing policy recovery metrics.

---

## 4. Defensible Research Gap Statement (Frozen)

> *Existing robot recovery benchmarks evaluate whether manipulation policies can complete tasks from intermediate failure states, typically reconstructed by replaying action prefixes or introducing ad-hoc runtime disturbances. However, these evaluations uniformly assume that recovery difficulty is governed solely by the instantaneous physical recovery state. It remains fundamentally unresolved whether a robot's recovery capability is invariant to the causal execution history that produced the failure. This research introduces a matched-state counterfactual evaluation protocol that tests whether robot policies exhibit significantly different detection, diagnosis, recovery, and completion performance when physically equivalent failure states are reached through different causal histories, and investigates whether current recovery benchmark rankings remain stable under causal control.*

