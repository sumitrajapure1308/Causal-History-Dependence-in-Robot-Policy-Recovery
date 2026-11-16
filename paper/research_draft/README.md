# Research Manuscript Draft & Final Package: Causal-History Dependence in Robot Policy Recovery

**Directory:** `paper/research_draft/`  
**Date:** 2026-11-12  
**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Status:** `BLOCKED — PENDING HUMAN INPUT & NATIVE LATEX COMPILATION`  

---

## 1. Directory Contents & Artifact Inventory

This directory contains the complete evidence-grounded research manuscript, metadata ledgers, and submission preparation bundle:

### Scientific Manuscript & Sources
- **`manuscript_v2.docx`**: **Version 2.0 Manuscript in Microsoft Word (.docx)** format, incorporating all newly applied methodologies (TOST practical equivalence, threshold sensitivity, horizon sensitivity, observation sensitivity, and contact regression), 6 embedded high-resolution figures, formatted tables, and PENDING HUMAN INPUT governance tags.
- **`manuscript.md`**: Complete academic manuscript in Markdown, with 191-word structured abstract, POMDP matched-state formulation, confirmatory benchmark results ($N=200$, 20,000 rollouts), TOST practical equivalence ($\Delta = \pm 0.05$), sensitivity analyses, mechanism findings, and all author metadata fields marked `PENDING HUMAN INPUT`.
- **`manuscript.tex`**: Complete LaTeX source formatted for IEEE RAS style (`ieeeconf` / `IEEEtran`), with author block marked `PENDING HUMAN INPUT` and zero fabricated credentials.
- **`references.bib`**: Verified BibTeX database containing 17 IEEE references.
- **`figures/`**: 14 publication figures (vector PDF and 600 DPI PNG) plus 4 sensitivity and mechanism figures and `figure_manifest.json`.
- **`evidence_map.csv`**: Claim-by-claim traceability matrix mapping 13 empirical claims to raw data, tests, and limitations.

### Author Metadata & Institutional Statements (Awaiting Human Input)
- **`author_metadata.md`**: Complete author specification ledger with slots for full legal names, author sequence, institutional affiliations, physical addresses, emails, ORCID iDs, corresponding author designations, and CRediT contributions (all marked `PENDING HUMAN INPUT`).
- **`funding_statement.md`**: Formal funding disclosure template (marked `PENDING HUMAN INPUT`).
- **`acknowledgments.md`**: Formal acknowledgment ledger for facilities, compute allocations, and collaborators (marked `PENDING HUMAN INPUT`).
- **`conflict_of_interest.md`**: IEEE financial and commercial conflict-of-interest disclosure ledger (marked `PENDING HUMAN INPUT`).
- **`ethics_statement.md`**: Detailed statement regarding simulation-only research, absence of human/animal subjects, and dual-use considerations (marked `PENDING HUMAN INPUT`).

### Packaging & Compilation Logs
- **`final_package_checklist.md`**: Comprehensive 10-point audit checklist covering author metadata, ORCID, PaperPlaza, LaTeX compilation, visual review, figures, references, supplementary material, multimedia, and submission readiness.
- **`build.log`**: Build toolchain detection log documenting the status of native LaTeX compilers.
- **`compile_manuscript_pdf.py`**: Python ReportLab typesetting script for internal draft reading. *(Note: Per project directive, ReportLab PDF output is for local reading only and is NOT accepted as evidence of native LaTeX compilation)*.
- **`manuscript_source.zip`**: Standalone source archive for compilation on external workstations equipped with TeX Live or MiKTeX.

---

## 2. Final Package Checklist Summary

| Item | Status | Key Evidence / Requirement |
|---|---|---|
| **1. Author Metadata** | `PENDING HUMAN INPUT` | Marked in `manuscript.md`, `manuscript.tex`, `author_metadata.md`. No synthetic identities. |
| **2. ORCID** | `PENDING HUMAN INPUT` | Authenticated 16-digit ORCID iDs required from all contributing authors. |
| **3. PaperPlaza Account** | `BLOCKED` | Automated account creation prohibited. Human author must register on `ras.papercept.net`. |
| **4. LaTeX Compilation** | `BLOCKED` | Native LaTeX compilers (`pdflatex`, `latexmk`) absent from system PATH. |
| **5. PDF Visual Review** | `BLOCKED` | Cannot be validated until native LaTeX compilation is executed on a TeX workstation. |
| **6. Figures** | `COMPLETE / VERIFIED` | 14 core figures + 4 sensitivity/mechanism figures verified and present in `figures/`. |
| **7. References** | `COMPLETE / VERIFIED` | 17 verified citations in `references.bib` matching in-text citations [1]–[17]. |
| **8. Supplementary** | `PREPARED / PENDING REVIEW` | Benchmark scripts, seeds, and execution logs preserved in repository. |
| **9. Multimedia** | `PREPARED / PENDING REVIEW` | Video generation scripts available in `scripts/generate_demo_video.py`. |
| **10. Submission Readiness** | `BLOCKED / NOT READY` | External submission strictly blocked pending real author metadata and human sign-off. |

---

## 3. Instructions for Human Authors

To advance this manuscript toward official IEEE submission:

1. **Provide Real Author Metadata:**
   Fill in verified legal names, affiliations, email addresses, and ORCID iDs in `paper/research_draft/author_metadata.md`.
2. **Select Declarations:**
   Review and sign off on `funding_statement.md`, `acknowledgments.md`, `conflict_of_interest.md`, and `ethics_statement.md`.
3. **Compile via Native LaTeX:**
   Transfer the archive `paper/research_draft/manuscript_source.zip` to a system with TeX Live or MiKTeX, and execute:
   ```bash
   latexmk -pdf manuscript.tex
   ```
4. **Visually Inspect PDF:**
   Confirm two-column balance, figure resolution, table readability, and reference formatting.
5. **Human Portal Registration:**
   The corresponding author must log into PaperPlaza (`https://ras.papercept.net/journals/ral`), register PINs, and manually upload the compiled manuscript and multimedia attachments.

---

## 4. Methodological Bounding & Anti-Fabrication Safeguards

- **Simulation-Only Bounding:** The study is simulation-only. All experiments were conducted in MuJoCo physics simulation; no real-robot hardware validation was performed.
- **Bounded Generalizability:** Results are bounded to the tested policies, tasks, conditions, and simulator.
- **Null Result Interpretation:** A nonsignificant result does not prove universal history invariance.
- **Observational Status of Mechanism:** Contact dynamics associations were derived observationally ($R^2_{\text{adj}} = 7.83\%$); causal confirmation requires controlled physical intervention experiments.
- **Zero External Action:** No external submission was performed.
