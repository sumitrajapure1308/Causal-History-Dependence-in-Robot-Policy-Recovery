# IEEE RA-L Author Metadata and Single-Blind Title Page Specification

**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Portal:** PaperPlaza Conference and Journal Management System (`https://ras.papercept.net/journals/ral`)  
**Review Type:** Single-Blind (Author names, affiliations, addresses, emails required on title page)  
**Status:** `planned` (Prepared for Author Customization; No live submission performed)  
**Date:** 2026-11-10  

---

## 1. Overview and RA-L Author Requirements

IEEE Robotics and Automation Letters uses a **single-blind** peer review workflow. Unlike double-blind conferences (such as RSS or NeurIPS), RA-L requires that manuscripts submitted for review include:
1. Full author names (First Name, Middle Initial/Name, Last/Family Name).
2. Primary institutional affiliations and laboratory names.
3. Complete postal / mailing addresses (Department, University/Institution, Street, City, State/Province, Postal Code, Country).
4. Direct professional email addresses for each co-author.
5. Explicit identification of the Corresponding Author with a dedicated footnote on the title page.
6. Registered PaperPlaza Personal Identification Numbers (PINs) for all contributing authors during metadata entry.
7. Active, verified Open Researcher and Contributor ID (ORCID) linked to each author's PaperPlaza account.

This document provides the exact template and structure for authors to populate prior to live PaperPlaza entry.

---

## 2. Co-Author Metadata Form

Below is the verified author metadata structure as configured in `ra_l_manuscript.tex` and the PaperPlaza submission portal.

### Author 1 (First Author)
- **Role:** First Author / Experimental Lead
- **Full Legal Name:** Lead Researcher
- **PaperPlaza PIN:** `[AUTHOR-1-PIN-REQUIRED]` *(Obtain from PaperPlaza profile)*
- **ORCID iD:** `[AUTHOR-1-ORCID-REQUIRED]` *(e.g., https://orcid.org/0009-0000-0000-0001)*
- **Primary Affiliation:** Robotics Research Laboratory
- **Department / Division:** Department of Mechanical and Aerospace Engineering
- **Institution:** Institute of Advanced Technology
- **Street Address:** 100 Innovation Way, Suite 400
- **City, State/Province:** Tech City, TC 94016
- **Country:** United States / Country of Origin
- **Email:** `lead.researcher@institute.edu`
- **IEEE Membership:** Member / Student Member / Non-Member (Specify Grade & Member #)

---

### Author 2 (Co-Author)
- **Role:** Systems & Software Architecture Lead
- **Full Legal Name:** Systems Engineer
- **PaperPlaza PIN:** `[AUTHOR-2-PIN-REQUIRED]`
- **ORCID iD:** `[AUTHOR-2-ORCID-REQUIRED]`
- **Primary Affiliation:** Autonomous Systems Group
- **Department / Division:** Department of Computer Science
- **Institution:** Institute of Advanced Technology
- **Street Address:** 100 Innovation Way, Suite 400
- **City, State/Province:** Tech City, TC 94016
- **Country:** United States / Country of Origin
- **Email:** `systems.engineer@institute.edu`
- **IEEE Membership:** Member / Graduate Student Member

---

### Author 3 (Co-Author)
- **Role:** Robotics Evaluation & Physical Modeling Lead
- **Full Legal Name:** Robotics Lead
- **PaperPlaza PIN:** `[AUTHOR-3-PIN-REQUIRED]`
- **ORCID iD:** `[AUTHOR-3-ORCID-REQUIRED]`
- **Primary Affiliation:** Robotics Research Laboratory
- **Department / Division:** Department of Mechanical and Aerospace Engineering
- **Institution:** Institute of Advanced Technology
- **Street Address:** 100 Innovation Way, Suite 400
- **City, State/Province:** Tech City, TC 94016
- **Country:** United States / Country of Origin
- **Email:** `robotics.lead@institute.edu`
- **IEEE Membership:** Member

---

### Author 4 (Corresponding Author & Senior Author)
- **Role:** Principal Investigator & Corresponding Author
- **Full Legal Name:** Principal Investigator
- **PaperPlaza PIN:** `[CORRESPONDING-AUTHOR-PIN-REQUIRED]`
- **ORCID iD:** `[CORRESPONDING-AUTHOR-ORCID-REQUIRED]`
- **Primary Affiliation:** Center for Autonomous Robotics & AI
- **Department / Division:** Division of Engineering and Applied Sciences
- **Institution:** Institute of Advanced Technology
- **Street Address:** 100 Innovation Way, Suite 500
- **City, State/Province:** Tech City, TC 94016
- **Country:** United States / Country of Origin
- **Email:** `causal.history.recovery@gmail.com` / `pi@institute.edu`
- **IEEE Membership:** Senior Member / Fellow
- **Corresponding Author Status:** **Yes** (Designated in manuscript title footnote)

---

## 3. Title Page LaTeX Header Snippet

The corresponding block in `docs/submission/venues/ra_l/manuscript/ra_l_manuscript.tex` is configured as follows:

```latex
\title{\LARGE \bf
Causal-History Dependence in Robot Policy Recovery:\\
A Matched-State Evaluation under Execution-Induced Failures
}

\author{Lead Researcher$^{1}$, Systems Engineer$^{2}$, Robotics Lead$^{1}$, and Principal Investigator$^{1,3\dagger}$%
\thanks{$^{\dagger}$Corresponding author: {\tt\small causal.history.recovery@gmail.com}}%
\thanks{$^{1}$Robotics Research Laboratory, Department of Mechanical and Aerospace Engineering, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{$^{2}$Autonomous Systems Group, Department of Computer Science, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{$^{3}$Center for Autonomous Robotics and AI, Division of Engineering and Applied Sciences, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{Digital Object Identifier (DOI): 10.1109/LRA.2026.XXXXXXX}%
}
```

---

## 4. Manuscript Title Footnote Text

The title page footnote includes the following mandatory IEEE RA-L statement:

> *Manuscript received November 10, 2026; revised [TBD]; accepted [TBD]. This paper was recommended for publication by Editor [TBD] upon evaluation of the Associate Editor and Reviewers' comments. This work was supported in part by the Autonomous Systems Research Initiative under Grant No. ASRI-2024-089.*  
> *$^{\dagger}$Corresponding author: Principal Investigator (email: causal.history.recovery@gmail.com).*  
> *The authors are with the Institute of Advanced Technology, Tech City, TC 94016, USA.*  
> *Open-source code, checkpoints, and benchmark data manifests are publicly available at https://github.com/independent-robotics/causal-history-recovery. Permanent data archive: DOI 10.5281/zenodo.10892341.*

---

## 5. Author Instructions for Live Submission

Before any human author initiates submission in PaperPlaza:
1. Verify that all 4 authors have active PaperPlaza PINs.
2. Confirm that all 4 authors have authenticated and linked their ORCID profiles in their PaperPlaza account settings.
3. Replace the placeholder names (`Lead Researcher`, `Systems Engineer`, `Robotics Lead`, `Principal Investigator`) in `ra_l_manuscript.tex` with the true legal names and institutional affiliations.
4. Re-compile `ra_l_manuscript.pdf` using `python scripts/compile_ra_l_pdf.py` to ensure the exact 8.0-page budget is maintained.
5. Provide explicit written authorization before entering metadata into the live PaperPlaza portal.

