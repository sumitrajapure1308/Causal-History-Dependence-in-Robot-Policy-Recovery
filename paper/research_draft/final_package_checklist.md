# Final Package Submission Checklist & Verification Audit

**Directory:** `paper/research_draft/final_package_checklist.md`  
**Date:** 2026-11-16  
**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L) / PaperPlaza  

---

## 1. Submission Gate Checklist

| Checklist Item | Current Status | Verification Details & Evidence | Action Required Before Submission |
|---|---|---|---|
| **1. Author Metadata Status** | `PARTIALLY COMPLETE` | Author name (`Sumit S. Rajapure`), email (`sumitrajapure2006@gmail.com`), ORCID (`0009-0009-8899-353X`), and personal funding confirmed. Zero synthetic identities fabricated. Remaining fields (affiliation, department, address, corresponding-author designation, acknowledgments, and conflict-of-interest confirmation) remain pending human input. | Human author to supply institutional affiliation, department, postal address, corresponding author confirmation, acknowledgments, and conflict sign-off. |
| **2. License Status** | `COMPLETE` | Repository dual-licensed: MIT License (`LICENSE`) for software/source code; Creative Commons Attribution 4.0 International (`LICENSE-DATA.md`) for documentation, figures, tables, datasets, and non-code research artifacts. Attributed to Sumit S. Rajapure. | None. Fully established. |
| **3. ORCID Status** | `COMPLETE` | Verified ORCID iD `0009-0009-8899-353X` recorded for author Sumit S. Rajapure. | None. Recorded in all author ledgers. |
| **4. PaperPlaza Account Status** | `BLOCKED` | No PaperPlaza accounts registered or credentials entered by automated systems, in strict adherence to ethics directives. | Human author must register personal account and obtain author PINs on `ras.papercept.net`. |
| **5. LaTeX Compilation Status** | `BLOCKED` | Native LaTeX toolchain (`pdflatex`, `latexmk`, `xelatex`, `lualatex`) is absent from the host Windows system PATH. (`compile_manuscript_pdf.py` exists using ReportLab for local reference, but per directive, ReportLab is **not** evidence of native LaTeX compilation). | Source files (`manuscript.tex`, `references.bib`, `figures/`) must be compiled via `latexmk -pdf manuscript.tex` on a standard TeX Live / MiKTeX workstation. |
| **6. PDF Visual-Review Status** | `BLOCKED` | Native LaTeX PDF visual inspection has not been completed because the native compiler is blocked. | Human authors must compile via LaTeX and visually inspect column balance, equation rendering, and figure legibility. |
| **7. Figure Status** | `COMPLETE / VERIFIED` | 14 core publication figures + 4 sensitivity/mechanism figures present in `paper/research_draft/figures/` with `figure_manifest.json`. All figures generated from verifiable simulation data pipelines. | Ready for final inclusion. |
| **8. Reference Status** | `COMPLETE / VERIFIED` | 17 verified references in `paper/research_draft/references.bib` matching in-text citations [1]–[17]. Zero fabricated DOIs, arXiv IDs, or authors. | Ready for final inclusion. |
| **9. Supplementary Status** | `PREPARED / PENDING HUMAN REVIEW` | Reproducible benchmark manifests, data processing scripts, smoke tests (74 passing), and configuration trees preserved in repository. | Human author to decide whether to attach as a single supplementary ZIP on PaperPlaza. |
| **10. Multimedia Status** | `PREPARED / PENDING HUMAN REVIEW` | Video generation scripts (`scripts/generate_demo_video.py`) and episode rollouts available in repository. | Human author to review and export final IEEE MP4 video attachment (< 30 MB) if submitting video. |
| **11. Submission Readiness Status** | `BLOCKED / NOT READY` | The scientific manuscript, data lineage, statistical analyses, licenses, and verified author contact/ORCID are completed. External submission remains blocked pending institutional affiliation/address, native LaTeX compilation, and human sign-off. | Complete items 1 and 4–6; obtain human author written authorization before any portal upload. |

---

## 2. Hard Stop Conditions & Safeguards

The automated pipeline enforces the following immutable stop rules:
1. **Zero External Access:** Automated agents will not connect to `ras.papercept.net`, open submission sessions, or upload files.
2. **Zero Synthetic Metadata:** No placeholder author names, affiliations, addresses, or PaperPlaza credentials may be fabricated.
3. **Audit Lineage:** Every scientific claim is traceable to raw data via `paper/research_draft/evidence_map.csv`.

---

## 3. Human Authorization Sign-Off

Final submission gate requires written confirmation from the human corresponding author:

- [x] Confirmed author name, personal email, ORCID iD, and personal funding updated
- [ ] Institutional affiliation, department, and postal address confirmed
- [ ] Corresponding author status confirmed
- [ ] Native LaTeX compilation verified with zero font or overfull hbox warnings
- [ ] Visual inspection of compiled two-column PDF completed
- [ ] Conflict of interest and funding statements signed off
- [ ] Explicit written authorization provided to submit to IEEE RA-L

**Authorized Human Sign-off:** PENDING HUMAN INPUT  
**Date:** PENDING HUMAN INPUT  
