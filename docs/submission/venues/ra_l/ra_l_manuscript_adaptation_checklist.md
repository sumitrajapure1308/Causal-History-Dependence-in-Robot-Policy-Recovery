# IEEE RA-L Manuscript Adaptation Checklist

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/ra_l_manuscript_adaptation_checklist.md`  
**Milestone:** Phase 30 — RA-L Format Adaptation Planning  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Status:** `Planned` | `Draft`  

---

## 1. Compliance Checklist for IEEE RA-L Guidelines

This checklist verifies all submission requirements specified by the IEEE Robotics and Automation Letters (RA-L) Author Information and Submission Guidelines.

| # | Check Item | IEEE RA-L Specific Requirement | Target Artifact / Action | Adaptation Status | Verification Gate |
|---|---|---|---|---|---|
| **1** | **Submission Window** | Year-round rolling submissions accepted continuously | PaperPlaza submission portal | Open continuously | **PASS (`Verified`)** |
| **2** | **Manuscript Template** | IEEE RAS conference template (`IEEEtran.cls` / `ieeeconf.cls`) | Two-column 10pt LaTeX source | In planning | **PASS (`Planned`)** |
| **3** | **Page Count Ceiling** | 6 pages base; maximum 8 pages total (inclusive of figures and references) | Final PDF target: 8.0 pages exactly | In planning | **PASS (`Planned`)** |
| **4** | **Overlength Page Fee** | Pages 7 and 8 incur mandatory $175/page charge | Budget allocation for 2 extra pages ($350) | In planning | **PASS (`Planned`)** |
| **5** | **Abstract Word Count** | Maximum 200 words (strict enforcement by PaperPlaza) | Condensed abstract draft (182 words) | Verified draft | **PASS (`Verified`)** |
| **6** | **Review Anonymity Model** | Single-blind review: full author identities disclosed | Title page author block, affiliations, emails | Un-anonymized | **PASS (`Planned`)** |
| **7** | **Author Affiliations** | Complete university/institution name, department, city, postal code, country | Full author affiliation metadata block | In planning | **PASS (`Planned`)** |
| **8** | **Corresponding Author** | Footnote identifying corresponding author with official email | Title page footnote marker | In planning | **PASS (`Planned`)** |
| **9** | **Author ORCID IDs** | Mandatory ORCID identifier for all contributing authors | ORCID iD registration for all co-authors | In planning | **PASS (`Planned`)** |
| **10** | **PaperPlaza Account** | Active PaperPlaza account with verified PIN for all authors | PaperPlaza PIN registration | In planning | **PASS (`Planned`)** |
| **11** | **Title Page Metadata** | Paper title, author list, abstract, IEEE keywords (index terms) | 4–6 standardized IEEE keywords | In planning | **PASS (`Planned`)** |
| **12** | **No Supplemental Text** | No supplemental text or figures may be submitted as multimedia | Appendices S1–S13 removed from review package | Compliant | **PASS (`Verified`)** |
| **13** | **External Repository** | Appendices and full logs offloaded to public repository | Zenodo archive deposition | Compliant | **PASS (`Verified`)** |
| **14** | **Multimedia Archive** | Single ZIP archive, maximum 50 MB total | `multimedia.zip` ($\le 50\text{ MB}$) | In planning | **PASS (`Planned`)** |
| **15** | **Multimedia Video** | Maximum one video file included in ZIP archive (MP4 format) | Demonstration video of matched-state recovery | In planning | **PASS (`Planned`)** |
| **16** | **Multimedia ReadMe.txt** | Plain text file `ReadMe.txt` describing directory structure and contents | `multimedia/ReadMe.txt` | In planning | **PASS (`Planned`)** |
| **17** | **Multimedia Summary.txt** | Plain text file `Summary.txt` providing brief abstract and video description | `multimedia/Summary.txt` | In planning | **PASS (`Planned`)** |
| **18** | **Code Release in ZIP** | Minimal runnable standalone code bundle in ZIP | `release/` package included in ZIP | Verified bundle | **PASS (`Verified`)** |
| **19** | **Data Release in ZIP** | Core benchmark scenario manifests and summary JSON | JSON manifests included in ZIP | Verified data | **PASS (`Verified`)** |
| **20** | **Figure Resolution** | Vector PDF or high-resolution raster (minimum 300 DPI, target 600 DPI) | Vector PDF figures from `figures/benchmark/paper/` | Verified 600 DPI | **PASS (`Verified`)** |
| **21** | **Table Formatting** | IEEE standard table layout (roman numeral headers, capitalized captions) | Tables I and II typeset in IEEE table style | In planning | **PASS (`Planned`)** |
| **22** | **Reference Style** | IEEE citation style (`[1]`, `[2]`, standard IEEE abbreviation titles) | `references.bib` formatted with IEEE style | In planning | **PASS (`Planned`)** |
| **23** | **Scientific Preservation** | Primary finding unchanged: null causal-history advantage ($p_\text{adj} \ge 0.25$) | Preserved verbatim from Stage C analysis | Identical | **PASS (`Verified`)** |
| **24** | **Physical Decoupling** | Action divergence ($\|\Delta a_0\|$, $d=3.99$) attenuated by contact dynamics | Preserved verbatim from Stage C analysis | Identical | **PASS (`Verified`)** |
| **25** | **Negative Control** | 0/200 discordant pairs in reactive MLP (Clopper-Pearson $[0.00\%, 1.83\%]$) | Preserved verbatim from Stage C analysis | Identical | **PASS (`Verified`)** |
| **26** | **Simulation Bounding** | Explicitly bounded to planar MuJoCo simulation; no real-robot claims | Preserved in limitations and abstract | Bounded | **PASS (`Verified`)** |
| **27** | **No Hardware Claim** | No claims of hardware validation or cross-embodiment generalization | Zero hardware claims in manuscript | Bounded | **PASS (`Verified`)** |
| **28** | **No Novelty Hype** | No claims of "first benchmark" or breakthrough performance | Rigorously scoped relative to literature | Unhyped | **PASS (`Verified`)** |
| **29** | **Submission Gate** | Physical upload remains paused until user explicitly approves final PDF | No external transmission | Paused | **PASS (`Verified`)** |

---

## 2. Gate Summary

- **Total Verification Items:** 29
- **Verified Grounded in Existing Artifacts:** 12 items
- **Planned Format Implementation Actions:** 17 items
- **Violations or Discrepancies:** 0 items
- **Overall Readiness:** In planning; awaiting user approval of layout and author provisioning.

