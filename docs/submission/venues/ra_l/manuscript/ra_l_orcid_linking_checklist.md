# IEEE RA-L ORCID Linking and Authentication Checklist

**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Requirement:** Mandatory IEEE Policy — All authors must have an authenticated ORCID iD linked to their PaperPlaza PIN.  
**Portal:** PaperPlaza Conference and Journal Management System (`https://ras.papercept.net`)  
**Strict Policy Directive:** Autonomous agents must NOT authenticate ORCID profiles or access third-party identity providers. This procedure must be executed directly by human authors.  
**Status:** `planned` (Author Action Required)  
**Date:** 2026-11-10  

---

## 1. IEEE Policy on ORCID Identifiers

In accordance with IEEE policy across all journals, letters, and transactions:
> *"All authors submitting manuscripts to IEEE journals must have an authenticated Open Researcher and Contributor ID (ORCID) iD associated with their account prior to manuscript acceptance. Corresponding authors must link their ORCID iD at the time of submission."*

PaperPlaza enforces this policy via an OAuth integration that directly authenticates with the official ORCID registry (`https://orcid.org`).

---

## 2. Step-by-Step Linking Instructions for Each Author

Each contributing co-author must perform the following one-time linkage:

1. **Log In to PaperPlaza:**
   - Go to `https://ras.papercept.net/`.
   - Enter your PaperPlaza PIN and password.
2. **Access Profile Information:**
   - Click on **"PIN Information"** or **"Update my profile"** in the main user menu.
3. **Initiate ORCID Authentication:**
   - Locate the field labeled **"ORCID iD"**.
   - Click the green button: **"Create or Connect your ORCID iD"**.
   - You will be redirected to the secure ORCID login page (`https://orcid.org/signin`).
4. **Authorize PaperPlaza:**
   - Sign in using your ORCID credentials (or institutional single sign-on).
   - Review permissions: PaperPlaza requests permission to retrieve your 16-digit ORCID identifier.
   - Click **"Authorize access"**.
5. **Verify Confirmation in PaperPlaza:**
   - After authorization, you will be redirected back to PaperPlaza.
   - Verify that your 16-digit ORCID appears with a green checkmark indicating **"Authenticated"** (e.g., `0000-0002-1825-0097`).
   - Click **"Submit / Update Profile"** to save changes.

---

## 3. Co-Author ORCID Status Tracking

| Author Name | Role | PaperPlaza PIN | 16-Digit ORCID iD | OAuth Verification Status |
|:------------|:-----|:--------------:|:-----------------:|:-------------------------:|
| Lead Researcher | First Author | `[PIN-1]` | `[ORCID-1]` | Pending Human Linkage |
| Systems Engineer | Co-Author | `[PIN-2]` | `[ORCID-2]` | Pending Human Linkage |
| Robotics Lead | Co-Author | `[PIN-3]` | `[ORCID-3]` | Pending Human Linkage |
| Principal Investigator | Corresponding Author | `[PIN-4]` | `[ORCID-4]` | Pending Human Linkage |

---

## 4. Verification Checkpoints Before Live Submission

Prior to final submission confirmation in PaperPlaza:
- [ ] Corresponding author's ORCID is fully authenticated.
- [ ] All 3 co-authors' ORCIDs are verified.
- [ ] ORCID URLs are verified not to return 404 on `https://orcid.org/<ORCID>`.
- [ ] No unlinked authors remain in the author metadata table.

