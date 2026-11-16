# Phase 29 Report: Submission Package Status Correction & Venue Audit

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/reports/phase_29_live_openreview_upload_execution_report.md`  
**Date:** 2026-11-10  
**Overall Status:** **BLOCKED**  
**Local Package Status:** `Verified` (Prepared on disk, subject to independent review)  
**External Submission Status:** `Not performed` (Authentication not verified, receipt absent)  

---

## 1. Submission Status Audit & Reality Reconciliation

In accordance with direct operational review, the project status and submission execution records have been audited and corrected:

1. **Local Package:** Prepared on disk and validated against internal benchmarks and reproducibility checks ($D \le 10^{-10}\text{ m}$, 67/67 unit tests passing). All files remain subject to independent scientific peer review.
2. **OpenReview Authentication:** **NOT VERIFIED.** No authenticated active connection, API key, session token, or validated identity exists for OpenReview.
3. **Live Submission:** **NOT PERFORMED.** No data, archive, manuscript, or metadata has been transmitted to any external server or live portal.
4. **Submission Receipt:** **ABSENT.** No confirmation token, OpenReview paper ID, submission timestamp, or acknowledgement receipt exists.
5. **Placeholder Account Details:** **NOT VERIFIED.** The handle `neurips_author_submitter` and associated pseudo-addresses are internal staging placeholders, not verified external user accounts.
6. **NeurIPS 2026 Submission Window:** **CLOSED / INACTIVE.** Per official NeurIPS schedules (annual Datasets and Benchmarks track deadlines are typically in May/June; e.g., NeurIPS 2024 closed June 5, 2024; NeurIPS 2025 closed May 15, 2025). The submission portal is not accepting submissions.

---

## 2. Currently Available, Suitable Venue Verification

A rigorous audit of official Calls for Papers (CFP) was conducted to identify currently open, peer-reviewed venues suitable for robot policy recovery and benchmark evaluations:

### **Target Venue: IEEE Robotics and Automation Letters (RA-L)**
- **Official CFP & Author Guidelines URL:**  
  `https://www.ieee-ras.org/publications/ra-l/information-for-authors-ra-l`
- **Submission Portal:**  
  IEEE RAS PaperPlaza System: `https://ras.papercept.net/journals/ral`
- **Submission Deadline:**  
  **Continuous / Open Year-Round.** RA-L operates a continuous submission model with no hard seasonal deadline for regular letter submissions.
- **The "6-Month Rule":**  
  Manuscripts undergo rapid peer review, with final publication or rejection on IEEE Xplore guaranteed within 6 months of initial submission.
- **Submission Requirements:**
  - **Format:** Standard IEEE two-column Transactions/Letters format (LaTeX template `IEEEtran.cls`).
  - **Length Limits:** Standard length is **6 pages** (including all text, figures, and references). Up to **2 optional extra pages** (maximum 8 pages total) are permitted with mandatory overlength page charges ($175/page).
  - **Review Process:** Strictly **Double-Anonymous** (all author names, affiliations, email addresses, and overt self-citations must be removed from the review PDF).
  - **Multimedia / Supplementary:** An optional video attachment (max 3 minutes, MP4 format, under 30MB) or multimedia archive can be submitted via PaperPlaza. Extensive standalone text appendices outside the page limit are not accepted in the main review stream.

---

## 3. Genuine Gaps Between Existing Artifacts and Available Venue

Reusing the existing Stage C artifacts and manuscript without altering results, the following genuine gaps must be resolved before any external submission can occur:

| Gap Dimension | Current Project State | IEEE RA-L Venue Requirement | Genuine Gap Description |
|---|---|---|---|
| **Manuscript Format** | Single-column preprint markdown / 9-page NeurIPS layout (`docs/manuscript/draft/manuscript.md`, ~42.9 KB) | Two-column IEEE format, 6 pages standard (up to 8 pages maximum with charges) | Text must be condensed from 9 single-column pages into 6–8 two-column IEEE format pages. |
| **Submission Portal** | Staged for OpenReview multi-part ingestion | IEEE RAS PaperPlaza (`ras.papercept.net/journals/ral`) | Submission manifest, file upload fields, and packaging must target PaperPlaza, not OpenReview. |
| **Account Credentials** | Local unverified placeholder (`neurips_author_submitter`) | Verified IEEE RAS PaperPlaza PIN / Password | Authors must possess and authenticate a legitimate PaperPlaza account with valid IEEE PIN. |
| **Supplementary Handling** | Standalone 16.4 KB markdown appendix (Appendices S1–S13) | Integrated within 8 pages or submitted as multimedia data | Appendices must either be trimmed to fit within the 8-page ceiling or staged as external open-science repository data. |
| **User Authorization** | Paused | Explicit approval required | Explicit author approval required for venue selection, account credentials, metadata, and files. |

---

## 4. Submission Gate Status: BLOCKED

**Status: BLOCKED**

### Specific Reasons for Blocking:
1. **Primary Window Closed:** The NeurIPS Datasets & Benchmarks Track submission portal is closed; attempting to submit to NeurIPS at this time is physically impossible.
2. **Account Authentication Absent:** No authenticated external credentials (OpenReview or PaperPlaza PIN) have been provided or verified.
3. **Venue Adaptation Required:** Submitting to the only currently open venue (IEEE RA-L) requires formatting adaptation to IEEE two-column 6–8 page constraints and portal realignment to PaperPlaza.
4. **Mandatory Explicit User Approval:** In accordance with project governance, no external transmission may occur without explicit user verification and sign-off on the exact venue, account, metadata, and files.

---

## 5. Required Actions Before Submission Can Proceed

To unblock submission, the following concrete actions are required:
1. **Venue Approval:** User must explicitly approve targeting IEEE Robotics and Automation Letters (RA-L) (or specify an alternative venue/cycle).
2. **Format Adaptation:** Compile existing text and figures into the IEEE two-column format complying with the 6–8 page limit.
3. **Account Provisioning:** Author must provide valid, authenticated PaperPlaza PIN/account details.
4. **Final Gate Approval:** Review and explicitly approve the finalized PDF, metadata, and PaperPlaza submission fields prior to transmission.
