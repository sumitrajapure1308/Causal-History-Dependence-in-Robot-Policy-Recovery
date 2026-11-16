# Formal Submission Decision & Strategic Venue Roadmap

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Repository Root:** `causal-history-recovery/`  
**Phase:** Phase 16 (Final Submission Decision & Journal-Readiness Audit)  
**Status:** `Submission Decision`, `Journal-Ready Evidence`, `Audited`, `Release Candidate`  
**Date:** November 10, 2026  

---

## 1. Executive Submission Decision

Based on the completed Phase 12 Stage C confirmatory benchmark ($20,000$ rollouts across 200 matched scenarios), the Phase 13 evidence package, the Phase 14 manuscript draft, the Phase 15 release package, and the Phase 16 multi-system audits:

**Formal Decision:** **CONDITIONAL APPROVAL FOR SUBMISSION TO TIER-2 BENCHMARK / ROBOTICS VENUES; PAUSED FOR HARDWARE-MANDATORY Q1 ROBOTICS JOURNALS.**

1. **Submission Readiness:** **READY.** The manuscript, supplementary materials, 14 paper figures at 600 DPI, 7 tables, 17 verified references, and 23-file release package in `release/` are 100% complete, reproducible, and internally consistent.
2. **Journal Readiness (Q1 Hardware Robotics - e.g. T-RO, IJRR):** **NOT READY.** General top-tier robotics journals strictly mandate physical robot experiments. Because this research is bounded as a simulation-based counterfactual benchmark, submitting to T-RO or IJRR at this stage presents a severe risk of rejection based on reality-gap concerns.
3. **Journal / Conference Readiness (Benchmark Tracks - e.g. NeurIPS Datasets & Benchmarks, RSS, IEEE RA-L):** **READY AS RELEASE CANDIDATE.** The methodological rigor, exact bitwise state matching ($D \le 10^{-10}	ext{ m}$), certified negative control (`reactive_mlp` 0/200 discordant), and pre-registered statistical power exceed standard expectations for benchmark and methodology submissions.

---

## 2. Multi-Dimensional Risk Synthesis

| Evaluation Domain | Risk Assessment | Identified Vulnerability | Built-in Mitigation & Protocol Safeguard |
| :--- | :---: | :--- | :--- |
| **Novelty Risk** | Low–Medium | Reviewers may perceive incremental advance over existing benchmarks. | Framed strictly as a matched-state causal-history evaluation protocol decoupling physical state from execution history; disclaims "first benchmark". |
| **Benchmark Overlap Risk** | Medium | Overlap with RoboRecover, LIBERO-Recover, and LIBERO-Pro2.0. | Sec. 4.1 and Table 1 explicitly audit prior benchmarks across 4 criteria, proving they conflate physical state with history prefix. |
| **Reproducibility Risk** | Negligible | Reviewers unable to reproduce results. | Standalone `release/` package with Dockerfile, environment specs, deterministic seeds, and automated smoke test passing in 2.5s. |
| **Statistical Risk** | Low | Low power or false positives from multiple testing. | Paired scenario inference unit ($N=200$), McNemar exact tests, Holm-Bonferroni FWER control, and transparent MDE reporting ($pprox 0.08$). |
| **Policy-Capability Risk** | Low–Medium | Reviewers questioning whether policies are capable of recovery. | Privileged oracle achieves 100% recovery; recovery-augmented policies exhibit 45% active corrective maneuvers; nominal GRU collapse audited. |
| **Generalization Risk** | Medium | Overclaiming universal history invariance across all manipulation. | Explicitly bounded to planar pushing; text clarifies that POMDPs with dynamically changing unobserved parameters require history. |
| **Real-Robot Reality Risk** | **High** | Absence of real-world physical robot deployment. | Prominently stated mandatory limitation sentence; simulation results explicitly bounded as simulation-based counterfactual evaluation. |
| **Cross-Simulator Risk** | Low–Medium | Evaluation conducted exclusively in MuJoCo physics. | Bitwise state matching ensures zero within-simulator drift; cross-simulator replication recommended as community future work. |

---

## 3. Recommended Submission Strategy & Target Venues

### Primary Target: NeurIPS Datasets & Benchmarks Track (or RSS / CoRL Benchmark Track)
- **Format:** Archival Paper + Supplementary Materials + Code/Data Repository.
- **Strategic Justification:** The NeurIPS Datasets & Benchmarks Track evaluates empirical methodology, data provenance, negative results, reproducibility checklists, and pre-registered scientific protocols. Our 20,000-rollout factorial design, certified negative control, and full Docker packaging are optimal fits.

### Secondary Target: IEEE Robotics and Automation Letters (RA-L)
- **Format:** Letter (6–8 pages) focused on the matched-state evaluation protocol and counterfactual findings.
- **Strategic Justification:** RA-L published RoboRecover (2024); our work directly builds upon, refines, and provides a methodologically rigorous counterfactual evaluation for this exact domain.

### Long-Term Target: IEEE Transactions on Robotics (T-RO) / IJRR (Phase 17+)
- **Prerequisite:** Physical hardware deployment (e.g. Franka Emika Panda robot with planar tactile/frictional manipulation) to bridge the reality gap.

---

## 4. Recommended Reviewer-Response Strategy

When addressing peer review feedback:
1. **"Why planar pushing instead of 6-DoF bi-manual manipulation?"**  
   *Response:* Planar pushing represents the foundational contact-rich benchmark where Coulomb friction, sticking/slipping transitions, and normal reaction forces can be mathematically modeled and bitwise matched ($D \le 10^{-10}$) without unmodeled joint compliance confounds.
2. **"Does this mean temporal history is useless for robot policies?"**  
   *Response:* No. We explicitly distinguish between fully observed physical state and POMDPs with unobserved dynamic parameters (e.g., hidden mass shifts, varying surface friction, fluid sloshing). Our findings demonstrate that when instantaneous physical state is known, execution history prefix provides no additional recovery advantage due to downstream physical contact bottlenecks.
3. **"Why is the binary recovery success rate low (1.0%–4.7%)?"**  
   *Response:* Planar recovery from severe kinematic deviations ($15.6^\circ$ yaw deflection) without privileged state access is inherently challenging. Privileged oracle reachability confirms that 100% of evaluated failure states are mechanically solvable, proving that low success reflects learned policy capability boundaries rather than task impossibility.

---

## 5. Final Recommendation

**Proceed to Phase 16 completion and await explicit user approval before initiating public repository deployment or journal portal upload.**
