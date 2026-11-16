# Formal Rebuttal Operations Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/post_submission/rebuttal_plan.md`  
**Milestone:** Phase 22 — Post-Submission Readiness and Reviewer-Response Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Post-submission readiness` | `Submission-ready evidence` | `Verified`  

---

## 1. Rebuttal Governance & Operating Protocol

This plan establishes the operational schedule, responsibilities, and procedural safeguards for the **14-day interactive author rebuttal period** on OpenReview for the **NeurIPS Track on Datasets and Benchmarks** (and secondary venues **RSS** / **IEEE RA-L**).

Operating rule: **Rebuttal responses must cite verified data from the frozen Stage C benchmark and disclaim unverified generalizations; zero new unvalidated models or ad-hoc experiments may be introduced during rebuttal.**

---

## 2. Rebuttal Action Register

| Rebuttal ID | Rebuttal Type | Rebuttal Deadline | Rebuttal Owner | Rebuttal Status | Rebuttal Risk | Rebuttal Mitigation | Rebuttal Required Action | Rebuttal Owner (Sign-Off) | Rebuttal Deadline (Window) |
|---|---|---|---|---|---|---|---|---|---|
| **REB-01** | **Review Ingestion & Triage** | $T+62$ Days (Day 2 of Rebuttal) | Lead Author | `Planned` | Overlooking critical reviewer questions or subtle methodological objections | Use structured query extraction script; catalog every bullet and sub-question | Extract all reviewer comments into point-by-point tracking sheet | Lead Author | $T+62$ Days |
| **REB-02** | **Empirical Evidence Mapping** | $T+64$ Days (Day 4 of Rebuttal) | Statistician | `Planned` | Reviewer skepticism on statistical power or null recovery effect | Map questions to frozen tables (`paper_tables.json`) and paired comparisons (`paired_comparisons.json`) | Generate exact data cross-references for Clopper-Pearson CIs and p-values | Statistician | $T+64$ Days |
| **REB-03** | **Point-by-Point Response Drafting** | $T+68$ Days (Day 8 of Rebuttal) | Lead Author | `Planned` | Defensive phrasing or overclaiming beyond simulation scope | Deploy pre-structured rebuttal templates from `reviewer_response_plan.md`; maintain respectful, evidence-first tone | Draft complete point-by-point author response for each reviewer | Lead Author | $T+68$ Days |
| **REB-04** | **Internal Co-Author Consensus Sign-Off** | $T+70$ Days (Day 10 of Rebuttal) | All Authors | `Planned` | Internal disagreement on response strategy or tone | Conduct mandatory author review meeting; require unanimous consensus on final text | Sign-off on finalized response text across all author stakeholders | Lead Author | $T+70$ Days |
| **REB-05** | **OpenReview Portal Dispatch & Discussion** | $T+72$ Days (Day 12 of Rebuttal) | Submitter | `Planned` | Portal outage or last-minute submission failure | Post responses $\ge 48$ hours prior to rebuttal close; engage actively in reviewer follow-up threads | Ingest official author response into OpenReview portal console | Submitter | $T+72$ Days |
| **REB-06** | **Score Tracking & Final Rebuttal Closure** | $T+74$ Days (Day 14 of Rebuttal) | Lead Author | `Planned` | Lingering reviewer misunderstandings before final area chair discussion | Monitor reviewer rating changes; provide concise 1-paragraph closing clarification if requested | Document final reviewer scores and area chair recommendations | Lead Author | $T+74$ Days |

---

## 3. Rebuttal Evidence Constraints

1. **Strict Non-Fabrication:** Never fabricate new p-values, post-hoc benchmark runs, or unrecorded simulator metrics during rebuttal.
2. **Boundary Preservation:** Reiterate that physical hardware trials are documented future work and that exact counterfactual restarts are a scientific capability unique to simulation.
3. **Reproducibility Reference:** Direct reviewers to the standalone smoke test (`release/smoke_test.py`) for instantaneous local verification.

---
*Rebuttal plan approved and certified by Autonomous Agent System.*
