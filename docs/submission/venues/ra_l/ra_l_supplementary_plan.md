# IEEE RA-L Supplementary Material Management Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/ra_l_supplementary_plan.md`  
**Milestone:** Phase 30 — RA-L Format Adaptation Planning  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Status:** `Planned` | `Draft`  

---

## 1. Verified RA-L Supplementary Rules

IEEE Robotics and Automation Letters (RA-L) enforces a strict policy regarding supplementary documents:
> **"No supplemental text or figures may be submitted as multimedia."**

Under this rule:
1. Authors are prohibited from uploading standalone PDF appendices (such as an extended appendix document) to PaperPlaza.
2. Authors are prohibited from smuggling supplementary text, proofs, or tables into the multimedia ZIP file.
3. Reviewers are instructed to evaluate the submission solely on the basis of the 6–8 page main paper and the approved multimedia elements (video/code/data).

---

## 2. Disposition of Existing Appendices (S1–S13)

The existing manuscript includes 13 supplementary sections (`docs/manuscript/supplementary_materials.md`, 16.4 KB). The following table defines the disposition of each section to ensure 100% compliance with RA-L rules:

| Appendix | Title / Content | Size / Scope | RA-L Disposition | Justification |
|---|---|---|---|---|
| **S1** | Mathematical Proofs of Intervention Semantics | 1.8 KB | **Integrate into Section III (Methodology)** | Core POMDP intervention definitions and hidden-state unrolling must be present in the main text for reviewers to understand the method. |
| **S2** | Simulator Contact Extraction Repeatability | 1.2 KB | **Condense into Section IV (Experimental Setup)** | Brief one-paragraph summary of contact force filtering and 0.0 impulse residual. |
| **S3** | Complete Scenario Generation Manifest | 2.5 KB | **External Zenodo Deposition** | Tabular catalog of 200 scenarios belongs in open dataset archive, not in review stream. |
| **S4** | Policy Training Hyperparameters & Architectures | 1.4 KB | **Integrate into Section IV (Table/Text)** | Essential network architecture specifications (MLP 2-layer, GRU 64-hidden) fit in Section IV. |
| **S5** | Complete Factorial Statistical Tables | 2.1 KB | **Condense into Section V (Tables I & II)** | Primary marginal and cell summaries fit into Tables I and II of main paper; raw per-seed numbers offloaded to Zenodo. |
| **S6** | Continuous Sensitivity Analysis & Ablations | 1.9 KB | **Integrate into Section V (Results)** | Key action divergence ($\|\Delta a_0\|$, $d=3.99$) and final error metrics integrated into main text. |
| **S7** | Hardware Blueprint & Physical Constraints | 1.6 KB | **Condense into Section VII (Limitations)** | Franka Panda hardware blueprint summarized in one paragraph under future work. |
| **S8** | Ethical Considerations | 0.8 KB | **Main Paper End Matter (Footnote/Section)** | Brief compliance statement (simulation research, no human/animal subjects). |
| **S9** | Conflict-of-Interest Statement | 0.6 KB | **Main Paper End Matter** | Mandatory IEEE COI statement included in main text footnote. |
| **S10** | Funding Statement | 0.6 KB | **Title Page Footnote** | Standard IEEE funding acknowledgment located on page 1 title block footnote. |
| **S11** | Author Contributions (CRediT) | 0.9 KB | **Main Paper End Matter** | CRediT contributor taxonomy placed before References. |
| **S12** | Data Availability Statement | 0.6 KB | **Main Paper End Matter** | Open-access data availability statement providing Zenodo DOI link. |
| **S13** | Code Availability Statement | 0.6 KB | **Main Paper End Matter** | Open-source MIT repository availability statement providing GitHub/Zenodo links. |

---

## 3. External Open-Science Archival Architecture

All supplementary materials not permitted in the PaperPlaza review stream will be hosted permanently on Zenodo:
- **Zenodo Deposit Package:** Complete raw 20,000 rollout records, per-scenario trajectories, full resolution figures (14 figures at 600 DPI), and extended analytical notebooks (Notebooks 01–76).
- **Paper Citation:** The main paper will reference this external repository via an open-science DOI in the Data Availability Statement on Page 8.
- **Reviewer Accessibility:** Reviewers may access the public Zenodo archive freely without violating PaperPlaza single-blind review or supplementary text restrictions.

