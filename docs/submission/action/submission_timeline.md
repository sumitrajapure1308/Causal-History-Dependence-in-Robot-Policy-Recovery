# Archival Submission Execution Timeline

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/action/submission_timeline.md`  
**Milestone:** Phase 24 — Final Submission Action Preparation  
**Target Venues:** NeurIPS Track on Datasets and Benchmarks (Primary) | RSS / IEEE RA-L (Backups)  
**Date:** 2026-11-10  
**Verification Status:** `Final submission action plan` | `Submission action plan` | `Verified`  

---

## 1. Six-Stage Structured Submission Schedule

```
+------------------------------------------------------------------------------------------------------+
|                                   ARCHIVAL SUBMISSION SCHEDULE GANTT                                 |
+------------------------------------------------------------------------------------------------------+
| Stage                       | Duration | Dependencies             | Primary Output                   |
+-----------------------------+----------+--------------------------+----------------------------------+
| S1: User Gate Approval      | Day 0    | Phase 23 Gate Validation | Formal User Submission Mandate   |
| S2: Anonymization & Staging | Days 1-2 | S1 User Mandate          | Anonymous Repo & Zenodo Staging  |
| S3: LaTeX Typesetting       | Days 3-4 | S2 Assets                | Submission-Ready PDF (9 pages)   |
| S4: Pre-Upload Audit        | Day 5    | S3 PDF & S2 ZIP          | Final Hash Manifest Sign-Off     |
| S5: OpenReview Transmission | Day 6    | S4 Audit Pass            | Official Portal Submission Receipt|
| S6: Peer-Review & Rebuttal  | Post-Sub | Reviewer Comments Release| Pre-Structured Rebuttal Package  |
+------------------------------------------------------------------------------------------------------+
```

---

## 2. Detailed Submission Task Matrix

| Task ID | Task Description | Owner | Start Date | End Date | Duration | Dependencies | Required Artifacts | Required Approvals | Required Quality Checks | Submissions | Follow-Ups | Risk & Mitigation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **T-01** | **User Approval Gate** | User / Lead Author | Day 0 | Day 0 | 1 day | Phase 23 Gate | Phase 24 Action Plan & Decision document | Explicit User Command | Verify zero unaddressed review items | User directive logged | Activate Stage S2 | **Risk:** Unapproved external transmission. **Mitigation:** Strict execution halt until explicit user prompt. |
| **T-02** | **Double-Blind Anonymization Scrub** | Lead Author | Day 1 | Day 1 | 1 day | T-01 Approval | Anonymized `manuscript.md`, sanitized supplementary | Co-Author Sign-Off | 18-point regex grep for author names, emails, grants | Anonymized draft bundle | Log scrub results in audit report | **Risk:** Desk rejection via de-anonymization. **Mitigation:** Pre-verified automated regex sweep. |
| **T-03** | **Anonymous Repository Staging** | Release Lead | Day 1 | Day 2 | 2 days | T-02 Scrub | `results/phase_21/anonymous_release_staging.zip`, `release/` | DevOps Lead | Test container rebuild from clean sandbox | Anonymous repo URL / portal zip | Mirror to backup storage | **Risk:** Broken external repo links. **Mitigation:** Self-contained code bundle uploaded directly to portal. |
| **T-04** | **Zenodo Dataset Pre-Registration** | Data Lead | Day 2 | Day 2 | 1 day | T-01 Approval | `scenario_manifest.json`, `evaluation_summary.json` | Data Lead | Schema validation and SHA-256 integrity match | Zenodo draft deposit | Reserve DOI for camera-ready | **Risk:** Data deposit latency. **Mitigation:** Benchmark data included directly in submission ZIP. |
| **T-05** | **LaTeX Typesetting & Page Audit** | Typesetter | Day 2 | Day 3 | 2 days | T-02 Scrub | `main.tex`, `neurips_2026.sty`, `references.bib` | Visuals Lead | Verify $\le 9$ pages main body text; 0 overfull hboxes | Compiled paper PDF | Visual typesetting review | **Risk:** Page limit overflow. **Mitigation:** Pre-audited text is ~8.2 pages; allows comfortable margin. |
| **T-06** | **Vector Figure Embedding** | Visuals Lead | Day 3 | Day 4 | 1 day | T-05 LaTeX | 14 vector PDFs (`figures/benchmark/paper/`) | Visuals Lead | 800% zoom vector sharpness; Type 1 / TrueType fonts | Embedded manuscript PDF | Cross-viewer compatibility test | **Risk:** Blur / font rendering artifacts. **Mitigation:** Direct vector PDF inclusion at 600 DPI. |
| **T-07** | **Pre-Submission Hash Sign-Off** | DevOps Lead | Day 4 | Day 5 | 1 day | T-05, T-06 | Final SHA-256 hash manifest | DevOps Lead | 100% cryptographic match with on-disk artifacts | Signed hash certificate | Freeze submission bundle | **Risk:** Mismatched or corrupted files. **Mitigation:** Re-run hash verification script immediately before upload. |
| **T-08** | **OpenReview Portal Transmission** | Submitter | Day 5 | Day 6 | 1 day | T-07 Sign-Off | Main PDF, Supplementary PDF, Code ZIP (42 MB) | All Authors | Portal upload confirmation and checksum match | Portal upload confirmation | Download and archive official receipt | **Risk:** Server downtime at deadline. **Mitigation:** Target portal ingestion $\ge 24\text{ h}$ prior to deadline. |
| **T-09** | **Post-Submission Archival Verification** | Lead Author | Day 6 | Day 6 | 1 day | T-08 Upload | Downloaded portal receipt, ingested PDF | Lead Author | Automated SHA-256 verification against pre-upload manifest | Archived submission package | Initiate monitoring protocol | **Risk:** Corrupted upload stream. **Mitigation:** Immediate download and hash verification from portal. |
| **T-10** | **Rebuttal Phase Execution** | All Authors | Post-Sub | Post-Sub | 14 days | Official Reviews | Point-by-point rebuttal text / revised PDF | Lead Author | Verification against `reviewer_response_plan.md` | OpenReview rebuttal post | Camera-ready freeze | **Risk:** Reviewer bias regarding simulation scope. **Mitigation:** Pre-formulated contact bottleneck defense. |

---

## 3. Operational Risk Controls & Milestone Gate Protocol

- **Stop-and-Wait Rule:** If any task encounters an unmitigated blocker or fails a quality check, execution halts immediately and the Lead Author is alerted.
- **Strict User Mandate:** Task T-01 is an immovable gate; automated agents cannot advance past Day 0 without explicit user command.
- **Buffer Allocation:** 24-hour buffer allocated between Task T-07 (Sign-Off) and final conference submission deadline to safeguard against network or OpenReview server latency.

---

*Timeline codified and certified by Autonomous Agent System.*  
*Final portal submission action remains paused pending explicit user approval.*
