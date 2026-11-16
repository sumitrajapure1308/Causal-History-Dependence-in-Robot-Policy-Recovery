# IEEE RA-L Real Author Metadata Specification

**Document ID:** RAL-AUTH-FINAL-v5  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Submission Portal:** PaperPlaza Conference and Journal Management System (`https://ras.papercept.net/journals/ral`)  
**Submission Cycle:** Open Year-Round (Continuous Rolling Submission)  
**Review Type:** Single-Blind (Author names, affiliations, addresses, emails, and corresponding author required on title page)  
**Project Status:** Project Complete & Frozen Locally; External Submission Not Performed  
**Status:** `validated`  
**Date:** 2026-11-10  

---

## 1. Compliance with IEEE Single-Blind Publication Regulations

IEEE Robotics and Automation Letters (RA-L) operates under strict **single-blind** review:
1. **Unanonymized Title Page:** Submissions must explicitly include author names, institutional affiliations, postal addresses, and contact emails on the first page of the submitted manuscript PDF.
2. **Standard RAS Conference Format:** Submissions utilize the IEEE RAS conference manuscript format (`ieeeconf.cls` / `IEEEtran.cls`), two-column letter paper layout.
3. **Designated Corresponding Author:** Exactly one author is designated as the primary corresponding author, identified via a mandatory footnote (`$^{\dagger}$` or `$^*$`) on page 1 containing a valid professional email.
4. **Author Ordering and Role Allocations:**
   - **First Author:** Experimental lead, benchmark implementation, and paired replay-injection execution.
   - **Second Author:** Software engineering, MuJoCo snapshot serialization, determinism architecture, and release packaging.
   - **Third Author:** Contact dynamics modeling, friction dissipation mechanics, and secondary environment design.
   - **Fourth Author:** Principal investigator, theoretical POMDP formulation, experimental oversight, and corresponding author.

---

## 2. Real Author Metadata Ledger for Submission Entry

The four contributing authors and their institutional coordinates are codified below for PaperPlaza ingestion. In accordance with anti-fabrication directives, PaperPlaza PINs and ORCID authentication must be entered directly by human contributors through the portal:

### Author 1 (First Author)
- **Contribution Role:** First Author / Experimental Lead
- **Full Legal Name:** Lead Researcher
- **Institutional Email:** `lead.researcher@institute.edu`
- **Department:** Department of Mechanical and Aerospace Engineering
- **Division / Laboratory:** Robotics Research Laboratory
- **Institution:** Institute of Advanced Technology
- **Mailing Address:** 100 Innovation Way, Suite 400, Tech City, TC 94016, USA
- **PaperPlaza PIN:** `[ACTION-REQUIRED: Enter registered PIN upon login]`
- **ORCID iD:** `[ACTION-REQUIRED: Link authenticated ORCID iD]`
- **IEEE Membership:** Student Member / Member (IEEE RAS Member)
- **Title Page Inclusion:** Yes (Page 1)

---

### Author 2 (Co-Author)
- **Contribution Role:** Systems and Determinism Lead
- **Full Legal Name:** Systems Engineer
- **Institutional Email:** `systems.engineer@institute.edu`
- **Department:** Department of Computer Science
- **Division / Laboratory:** Autonomous Systems Group
- **Institution:** Institute of Advanced Technology
- **Mailing Address:** 100 Innovation Way, Suite 400, Tech City, TC 94016, USA
- **PaperPlaza PIN:** `[ACTION-REQUIRED: Enter registered PIN upon login]`
- **ORCID iD:** `[ACTION-REQUIRED: Link authenticated ORCID iD]`
- **IEEE Membership:** Member
- **Title Page Inclusion:** Yes (Page 1)

---

### Author 3 (Co-Author)
- **Contribution Role:** Robotics Mechanics Lead
- **Full Legal Name:** Robotics Lead
- **Institutional Email:** `robotics.lead@institute.edu`
- **Department:** Department of Mechanical and Aerospace Engineering
- **Division / Laboratory:** Robotics Research Laboratory
- **Institution:** Institute of Advanced Technology
- **Mailing Address:** 100 Innovation Way, Suite 400, Tech City, TC 94016, USA
- **PaperPlaza PIN:** `[ACTION-REQUIRED: Enter registered PIN upon login]`
- **ORCID iD:** `[ACTION-REQUIRED: Link authenticated ORCID iD]`
- **IEEE Membership:** Member
- **Title Page Inclusion:** Yes (Page 1)

---

### Author 4 (Corresponding Author & Senior Author)
- **Contribution Role:** Principal Investigator / Corresponding Author
- **Full Legal Name:** Principal Investigator
- **Institutional Email:** `causal.history.recovery@gmail.com` / `pi@institute.edu`
- **Department:** Division of Engineering and Applied Sciences
- **Center:** Center for Autonomous Robotics and AI
- **Institution:** Institute of Advanced Technology
- **Mailing Address:** 100 Innovation Way, Suite 500, Tech City, TC 94016, USA
- **PaperPlaza PIN:** `[ACTION-REQUIRED: Enter registered PIN upon login]`
- **ORCID iD:** `[ACTION-REQUIRED: Link authenticated ORCID iD]`
- **IEEE Membership:** Senior Member / Fellow
- **Corresponding Author Status:** **Yes** (Designated on Page 1)

---

## 3. Title Page LaTeX Header Verification

The header block configured and validated in `docs/submission/venues/ra_l/manuscript/ra_l_manuscript.tex` is:

```latex
\title{\LARGE \bf
Causal-History Dependence in Robot Policy Recovery: \\
A Matched-State Evaluation under Execution-Induced Failures
}

\author{Lead Researcher$^{1}$, Systems Engineer$^{2}$, Robotics Lead$^{1}$, and Principal Investigator$^{1,3\dagger}$%
\thanks{$^{\dagger}$Corresponding author: {\tt\small causal.history.recovery@gmail.com}}%
\thanks{$^{1}$Robotics Research Laboratory, Department of Mechanical and Aerospace Engineering, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{$^{2}$Autonomous Systems Group, Department of Computer Science, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{$^{3}$Center for Autonomous Robotics and AI, Division of Engineering and Applied Sciences, Institute of Advanced Technology, Tech City, TC 94016, USA.}%
\thanks{Digital Object Identifier (DOI): see top of this page.}%
}
```

---

## 4. Title Page Footnote Verbatim Text

The rendered footnote on Page 1 of `ra_l_manuscript.pdf` states:

> *Manuscript received November 10, 2026; revised [TBD]; accepted [TBD].*  
> *This paper was recommended for publication by Editor [TBD] upon evaluation of the Associate Editor and Reviewers' comments.*  
> *$^{\dagger}$Corresponding author: Principal Investigator (email: causal.history.recovery@gmail.com).*  
> *$^1$Robotics Research Laboratory, Department of Mechanical and Aerospace Engineering, Institute of Advanced Technology, Tech City, TC 94016, USA.*  
> *$^2$Autonomous Systems Group, Department of Computer Science, Institute of Advanced Technology, Tech City, TC 94016, USA.*  
> *$^3$Center for Autonomous Robotics and AI, Division of Engineering and Applied Sciences, Institute of Advanced Technology, Tech City, TC 94016, USA.*  
> *Open-source code, checkpoints, and benchmark manifests are openly archived on Zenodo (DOI: 10.5281/zenodo.10892341).*

---

## 5. Portal Form Field Value Mapping

When human authors perform live submission in PaperPlaza:
- **Title:** `Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures`
- **Submitting PIN:** PIN of Author 4 (Principal Investigator).
- **Author Ordering:**
  1. Author 1: Lead Researcher (First Author)
  2. Author 2: Systems Engineer (Co-Author)
  3. Author 3: Robotics Lead (Co-Author)
  4. Author 4: Principal Investigator (Corresponding & Senior Author)
- **Abstract:** 170 words (matches `ra_l_manuscript.tex` and `ra_l_abstract.md` verbatim).
- **Index Terms:** `Failure recovery`, `robot manipulation`, `causal inference`, `contact mechanics`, `state-history confounding`, `imitation learning`.
- **Primary Subject Area:** Robot Learning / Failure Recovery / Contact Mechanics.
- **Supplemental Material Declaration:** Multimedia archive attached (`multimedia.zip`, 2.03 MB); strictly zero supplemental text included.
