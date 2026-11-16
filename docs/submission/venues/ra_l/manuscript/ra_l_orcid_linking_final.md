# IEEE RA-L ORCID Linking and Authentication Specification (Final)

**Document ID:** RAL-ORCID-FINAL-v5  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Requirement:** Mandatory IEEE Policy — All authors must link an authenticated ORCID iD to their PaperPlaza PIN.  
**Portal:** PaperPlaza Conference and Journal Management System (`https://ras.papercept.net`)  
**Strict Policy Directive:** Autonomous agents must NOT authenticate ORCID accounts or execute external OAuth transactions. All linkage steps must be performed directly by human authors.  
**Project Status:** Project Complete & Frozen Locally; External Submission Not Performed  
**Status:** `validated`  
**Date:** 2026-11-10  

---

## 1. IEEE Mandatory ORCID Mandate Overview

IEEE policy strictly mandates that **all published authors** possess an authenticated Open Researcher and Contributor ID (ORCID iD). For IEEE Robotics and Automation Letters (RA-L) submissions via PaperPlaza:
1. **Authenticated Linking:** An ORCID identifier cannot simply be typed as a text string into PaperPlaza; it must be authenticated via the official ORCID OAuth 2.0 API.
2. **Pre-Submission Requirement:** Co-authors should complete their ORCID authentication prior to manuscript submission or within the revision window. The corresponding author cannot finalize camera-ready publication without all co-author ORCIDs verified.
3. **Persistent Attribution:** The authenticated ORCID guarantees permanent, disambiguated attribution on IEEE Xplore and cross-indexing databases.

---

## 2. Co-Author ORCID Verification Roster

| Author Role | Legal Name | Institutional Email | ORCID Identifier Status | Authentication Method |
|---|---|---|---|---|
| **Author 1 (First Author)** | Lead Researcher | `lead.researcher@institute.edu` | Action Required by Human Author | OAuth 2.0 handshake via PaperPlaza |
| **Author 2 (Co-Author)** | Systems Engineer | `systems.engineer@institute.edu` | Action Required by Human Author | OAuth 2.0 handshake via PaperPlaza |
| **Author 3 (Co-Author)** | Robotics Lead | `robotics.lead@institute.edu` | Action Required by Human Author | OAuth 2.0 handshake via PaperPlaza |
| **Author 4 (Corresponding Author)** | Principal Investigator | `causal.history.recovery@gmail.com` | Action Required by Human Author | OAuth 2.0 handshake via PaperPlaza |

---

## 3. Human Step-by-Step ORCID Authentication Procedure

Human authors must follow these verified steps to link their ORCID to their PaperPlaza PIN:

1. **Access PaperPlaza Profile:**
   - Go to `https://ras.papercept.net`.
   - Log in using your personal PIN and password.
2. **Initiate OAuth Linkage:**
   - Under the **Personal Information** or **Profile Maintenance** menu, locate the **"ORCID Identification"** section.
   - Click the green button: **"Create or Connect your ORCID iD"**.
3. **Complete ORCID Authorization:**
   - A secure pop-up window opens from `https://orcid.org/signin`.
   - Enter your ORCID account credentials (or register a new ORCID at `https://orcid.org/register`).
   - Click **"Authorize access"** to permit PaperPlaza (`papercept.net`) to read your trusted ORCID identifier.
4. **Confirm Verification:**
   - PaperPlaza displays a green verification checkmark and stores the 16-digit hyphenated format (`0000-XXXX-XXXX-XXXX`).
   - The verified status immediately associates with your PaperPlaza PIN for all current and future RA-L submissions.
