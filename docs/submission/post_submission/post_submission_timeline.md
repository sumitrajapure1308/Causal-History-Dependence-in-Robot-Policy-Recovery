# Post-Submission Timeline & Operational Lifecycle

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Document:** `docs/submission/post_submission/post_submission_timeline.md`  
**Milestone:** Phase 22 — Post-Submission Readiness and Reviewer-Response Preparation  
**Date:** 2026-11-10  
**Verification Status:** `Post-submission readiness` | `Submission-ready evidence` | `Verified`  

---

## 1. Post-Submission Lifecycle Architecture

The post-submission schedule structures the end-to-end timeline from initial portal upload through peer-review, rebuttal, decision notification, camera-ready preparation, and archival open-access deposition.

---

## 2. Detailed Lifecycle Task Schedule

| Task ID | Task Description | Owner | Start Date | End Date | Duration | Dependencies | Required Artifacts | Required Approvals | Required Checks | Required Submissions | Required Follow-Ups | Primary Risk | Mitigation Strategy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P-01** | **Upload Receipt Archival & Checksum Match** | Lead Author | 2026-11-10 | 2026-11-10 | 1 Day | User upload clearance | OpenReview receipt PDF, `post_submission_manifest.md` | Author sign-off | Re-download uploaded files; verify SHA-256 match | OpenReview confirmation | Log receipt in repository | Upload stream corruption | Automated checksum comparison against local manifest |
| **P-02** | **Desk Screening & Formatting Compliance** | Visuals Lead | 2026-11-11 | 2026-11-24 | 14 Days | P-01 receipt | Compiled manuscript PDF (<= 9 pages) | Area Chair screening | Check typography, font embedding, margin bounds | None | Confirm pass of administrative filter | Desk reject for formatting drift | Pre-typeset 8.2 pages using official style |
| **P-03** | **Review Window & Discussion Monitoring** | Submitter | 2026-11-25 | 2027-01-09 | 45 Days | P-02 screening | OpenReview discussion portal | Submitter tracking | Check weekly for administrative announcements | None | Alert authors to incoming messages | Missed chair inquiries | Automated email forwarding + weekly portal checks |
| **P-04** | **Review Release & Question Triage** | All Authors | 2027-01-10 | 2027-01-12 | 3 Days | Official review release | Reviewer scorecards, `reviewer_response_plan.md` | Author consensus | Categorize reviewer concerns into 6 pre-structured themes | None | Draft response outlines | Misinterpreting reviewer critiques | Ground triage in pre-staged response matrices |
| **P-05** | **Rebuttal Authoring & Empirical Evidence Mapping** | Lead Author / Co-Authors | 2027-01-13 | 2027-01-20 | 8 Days | P-04 triage | Rebuttal drafts, Stage C data tables | All Authors sign-off | Verify all empirical claims match Stage C benchmark data | Draft text in OpenReview console | Internal peer-review proofreading | Inconsistent empirical numbers | Cite exact verified figures and p-values from Section 4 |
| **P-06** | **Interactive Discussion & Rebuttal Dispatch** | All Authors | 2027-01-21 | 2027-01-24 | 4 Days | P-05 sign-off | Finalized rebuttal text | Author consensus | Confirm respectful, rigorous tone; zero new unverified experiments | Official OpenReview rebuttal posts | Monitor reviewer score updates | Reviewer pushback on null effect / simulation | Cite negative control (0/200 discordant) & contact normal damping |
| **P-07** | **Camera-Ready Typesetting & De-Anonymization** | Visuals Lead | 2027-02-01 | 2027-02-15 | 15 Days | Notification of Acceptance | Final LaTeX source, author bio blocks | All Authors sign-off | Verify full author names, institutional affiliations, grant IDs | Camera-ready PDF | Visual and font validation | De-anonymization formatting drift | Use pre-budgeted camera-ready template |
| **P-08** | **Zenodo Open-Access DOI Deposition** | Data Lead / Release Lead | 2027-02-16 | 2027-02-16 | 1 Day | P-07 camera-ready | 4-file deposit bundle (125,486 bytes) | Lead Author sign-off | Verify live Zenodo DOI resolution; check zip download | Public Zenodo dataset release | Link persistent DOI into camera-ready paper | Broken links or download errors | Deploy pre-staged deposit payload cataloged in `zenodo_doi_reservation.md` |

---
*Timeline approved and certified by Autonomous Agent System.*
