# Submission Execution Timeline & Operations Schedule

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/execution/submission_execution_timeline.md`  
**Milestone:** Phase 20 — Final Submission Execution Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Submission execution package` | `Submission-ready evidence` | `Verified`  

---

## 1. Timeline Structure & Operational Phases

The execution timeline coordinates all pre-submission, upload, verification, and post-submission activities for the target venue: **NeurIPS Track on Datasets and Benchmarks** (with backup venues **RSS** and **IEEE RA-L**).

Operating rule: **All execution steps beyond packaging freeze remain paused until explicit user approval is granted.**

---

## 2. Detailed Task Schedule

| Task ID | Task Description | Owner | Start Date | End Date | Duration | Dependencies | Required Artifacts | Required Approvals | Required Checks | Required Submissions | Required Follow-Ups | Primary Risk | Mitigation Strategy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **T-01** | **Packaging Freeze & User Approval Gate** | User / Lead Author | 2026-11-10 | 2026-11-10 | 1 Day | Phase 19 action plan | `phase_20_file_hashes.json`, Execution package | Explicit User Approval | Check all 29 components present on disk | None | Archive local git-free hash ledger | Unapproved external transmission | Enforce strict pause; zero automatic network requests |
| **T-02** | **Double-Blind Anonymization Scrub** | Lead Author | 2026-11-11 | 2026-11-11 | 1 Day | T-01 approval | Anonymized `manuscript.md`, stripped `references.bib` | Author sign-off | Regex search for author names, emails, grants | None | Verify zero self-identifying phrasing | Desk rejection via de-anonymization | Double-blind inspection protocol |
| **T-03** | **Release Package Staging & Zenodo Preparation** | Release Lead | 2026-11-12 | 2026-11-12 | 1 Day | T-02 scrub | `release.zip` (35 MB), Zenodo metadata draft | Data Lead approval | Verify `release/smoke_test.py` passes in Docker | Supplementary ZIP bundle | Generate SHA-256 checksum file | Code link failure during review | Bundle self-contained code ZIP directly to OpenReview |
| **T-04** | **LaTeX Typesetting & Vector PDF Embedding** | Visuals Lead | 2026-11-13 | 2026-11-13 | 1 Day | T-02 scrub | Compiled `manuscript.pdf`, 14 vector figures | Visuals Lead sign-off | Page count $\le 9$ pages main body; 600 DPI vector rendering | Formatted submission PDF | Visual inspection of typography and fonts | Formatting rejection / overflow | Strict page budget: 8.2 pages main text + references + checklist |
| **T-05** | **Pre-Flight Ingestion & OpenReview Submission** | Submitter | 2026-11-14 | 2026-11-14 | 1 Day | T-03, T-04 | Final PDF, Supplementary PDF, Code ZIP | Lead Author approval | Verify metadata matches manuscript (250-word abstract) | Upload to OpenReview system | Save official confirmation receipt | Server overload at final deadline | Submit $\ge 24$ hours prior to deadline cutoff |
| **T-06** | **Post-Upload Verification & Archival** | Lead Author | 2026-11-15 | 2026-11-15 | 1 Day | T-05 submission | OpenReview submission receipt PDF | Lead Author sign-off | Re-download uploaded files; match SHA-256 against manifest | Official submission receipt archive | Log receipt in `docs/submission/execution/` | Corrupted upload on server | Automated checksum match against local files |
| **T-07** | **Rebuttal Phase Monitoring & Rebuttal Dispatch** | All Authors | Review Release Date | Rebuttal Close Date | 14 Days | Official review release | `reviewer_response_template.md` | All Authors consensus | Verify all empirical answers match Stage C benchmark data | OpenReview rebuttal responses | Track reviewer rating changes | Reviewer pushback on null effect / simulation | Pre-structured rebuttal matrices citing normal contact damping |

---

## 3. Critical Path Analysis

$$\text{T-01 (Gate)} \longrightarrow \text{T-02 (Scrub)} \longrightarrow \begin{cases} \text{T-03 (Code Staging)} \\ \text{T-04 (Typesetting)} \end{cases} \longrightarrow \text{T-05 (OpenReview)} \longrightarrow \text{T-06 (Verification)} \longrightarrow \text{T-07 (Rebuttal)}$$

Total operational lead time prior to deadline: **5 Days** (buffer of $\ge 24$ hours maintained before venue portal closure).

---
*Timeline codified and certified by Autonomous Agent System.*

