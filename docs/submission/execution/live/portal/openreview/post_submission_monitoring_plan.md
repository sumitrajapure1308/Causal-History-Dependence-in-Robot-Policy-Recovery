# Post-Submission Monitoring & Lifecycle Plan (Live OpenReview Upload)

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/execution/live/portal/openreview/post_submission_monitoring_plan.md`  
**Milestone:** Phase 28 — Live OpenReview Upload  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Post-submission monitoring` | `Live OpenReview upload` | `Verified`  

---

## 1. Post-Submission Governance & Lifecycle Objectives

This plan establishes the operational lifecycle protocol following archival ingestion into the **NeurIPS Track on Datasets and Benchmarks** via the OpenReview platform (and secondary fallback targets **RSS** and **IEEE RA-L**).

The objective is to guarantee seamless tracking, immediate verification, disciplined rebuttal deployment, and archival deposition without compromising project rules or empirical integrity.

---

## 2. Exhaustive Follow-Up Register

| Venue | Submission Type | Submission Deadline | Required Follow-Ups | Follow-Up Type | Follow-Up Deadline | Follow-Up Owner | Follow-Up Status | Operational Risk | Concrete Mitigation |
|---|---|---|---|---|---|---|---|---|---|
| **NeurIPS D&B** | Benchmark Track Paper | Official Track Deadline | **F-01: OpenReview Receipt Archival & Checksum Verification** | Technical Integrity Audit | Submission Day ($T+0\text{h}$) | Lead Author | `Planned` | Server upload corruption or silent file truncation | Re-download files from OpenReview immediately; verify byte-for-byte SHA-256 match against `openreview_submission_manifest.md` |
| **NeurIPS D&B** | Benchmark Track Paper | Official Track Deadline | **F-02: OpenReview Desk Screening & Formatting Monitoring** | Administrative Compliance | $T+14$ Days post-deadline | Lead Author | `Planned` | Desk rejection for page overflow or accidental de-anonymization | Pre-audited 8.2-page main text within 9-page limit; 18-point anonymization audit passed |
| **NeurIPS D&B** | Benchmark Track Paper | Official Track Deadline | **F-03: OpenReview Forum Discussion Triage** | Peer Review Monitoring | Review Release Date ($T+60$ Days) | All Authors | `Planned` | Reviewer skepticism regarding null binary recovery parity ($p_\text{adj} \ge 0.2500$) | Deploy pre-staged empirical rebuttal in `reviewer_response_plan.md` citing negative control zero discordance (0/200 pairs) |
| **NeurIPS D&B** | Benchmark Track Paper | Official Track Deadline | **F-04: Formal OpenReview Rebuttal Dispatch & Interaction** | Rebuttal Execution | Rebuttal Close Date ($T+74$ Days) | Lead Author / Co-Authors | `Planned` | Reviewer demand for physical Franka Panda hardware validation | Deploy pre-formulated response citing physical counterfactual restart impossibility ($D \le 10^{-10}\text{ m}$ achievable only in simulation) |
| **NeurIPS D&B** | Benchmark Track Paper | Official Track Deadline | **F-05: Camera-Ready Finalization & OpenReview Release** | Archival Camera-Ready | Camera-Ready Deadline ($T+90$ Days) | Release Lead / Data Lead | `Planned` | Link rot or delayed open-access dataset availability | Mint live Zenodo DOI using pre-staged metadata in `zenodo_doi_reservation.md`; de-anonymize author block |
| **RSS / RA-L** | Alternative Submission | Venue Specific Deadline | **F-06: Contingency Fallback Deployment** | Venue Re-Routing | Upon Final Decision | All Authors | `Planned` | Potential rejection from primary benchmark track | Immediate re-submission using pre-compiled venue packages in `docs/submission/venues/robotics_science_systems/` or `ieee_ral/` |

---

## 3. Communication & OpenReview Alert Protocol

- **Weekly Forum Monitoring:** Lead Author monitors the OpenReview submission forum weekly during the review window ($T+14$ to $T+60$ days).
- **Official Comment Response Window:** Any clarification requested by Area Chairs or Reviewers on OpenReview will be drafted within 24 hours using pre-verified Stage C evidence.
- **Strict Evidence Adherence:** All OpenReview public and private comments must cite verified data from `results/phase_12_stage_c/` and never fabricate new experiments or ad-hoc p-values.

---

*OpenReview monitoring plan approved and certified by Autonomous Agent System.*  
*Physical OpenReview upload action remains strictly paused pending explicit user approval.*

