# IEEE RA-L Multimedia Submission Plan

**Project:** Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures  
**Package:** `causal_history_recovery`  
**Document:** `docs/submission/venues/ra_l/ra_l_multimedia_plan.md`  
**Milestone:** Phase 30 — RA-L Format Adaptation Planning  
**Target Venue:** IEEE Robotics and Automation Letters (RA-L)  
**Date:** 2026-11-10  
**Status:** `Planned` | `Draft`  

---

## 1. Verified RA-L Multimedia Regulations

IEEE Robotics and Automation Letters (RA-L) permits supplementary multimedia submission under strict technical conditions:
1. **Single ZIP Archive:** All multimedia components must be packaged into **exactly one ZIP archive**.
2. **Maximum File Size:** The archive must not exceed **50 MB** in total size.
3. **Mandatory Plain Text Metadata:** The archive root must contain exactly two specific text files:
   - `ReadMe.txt`: Detailed description of directory contents, software setup, and execution instructions.
   - `Summary.txt`: Brief paper summary, contributor list, and video narration transcript / description.
4. **Allowed Contents:**
   - Maximum **one video** file.
   - Datasets and benchmark manifests.
   - Source code and reproduction scripts.
   - README files.
5. **Strictly Prohibited:** **No supplemental text or figures** (e.g., PDF appendices, draft papers, extra result graphs) may be submitted inside the multimedia archive.

---

## 2. Multimedia Archive Directory Layout (`multimedia.zip`)

```
multimedia.zip/
├── ReadMe.txt                                 # Mandatory: Setup & directory documentation
├── Summary.txt                                # Mandatory: Abstract & video description
├── video/
│   └── causal_history_recovery_demo.mp4       # Single video: matched-state demo (<= 25 MB)
├── code/
│   ├── src/                                   # Standalone package causal_history_recovery
│   ├── models/checkpoints/                    # 4 pre-trained PyTorch policy models (.pt)
│   ├── smoke_test.py                          # Automated 2.7s smoke test
│   ├── environment.yml                        # Conda environment definition
│   ├── Dockerfile                             # Containerized reproduction environment
│   └── pyproject.toml                         # Package build metadata
└── data/
    ├── scenario_manifest_representative.json  # 4 representative matched scenarios
    ├── evaluation_summary.json                # Stage C aggregate performance summary
    └── paired_comparisons_summary.json        # Paired McNemar & Wilcoxon results
```

---

## 3. Detailed Specification of Multimedia Components

### 3.1. Demonstration Video (`video/causal_history_recovery_demo.mp4`)
- **Format:** MP4 (H.264 video codec, AAC audio codec, 1920x1080 resolution, 30 fps).
- **Duration:** 2 minutes 30 seconds (maximum allowable: 3 minutes).
- **Target File Size:** ~20–25 MB.
- **Narrative Storyboard:**
  1. *0:00–0:30 (Motivation & Problem):* Illustrates execution-induced failure (off-center contact slip) and demonstrates how observational comparisons conflate physical state with history.
  2. *0:30–1:00 (Matched-State Methodology):* Visualizes the Paired Replay-Injection Matching protocol, demonstrating identical physical state restoration ($D \le 10^{-10}\text{ m}$) across Conditions B0 (nominal replay) and B4 (matched direct injection).
  3. *1:00–1:45 (Empirical Action Divergence vs Contact Attenuation):* Shows the immediate motor action divergence ($\|\Delta a_0\| = 0.0038\text{ m/step}$) of recurrent policies, followed by physical interaction showing normal contact forces and surface friction dampening the divergence prior to goal dwell.
  4. *1:45–2:30 (Benchmark Summary):* Displays confirmatory recovery trajectories across all 4 policies, concluding with the physical contact bottleneck finding and simulation bounds.

### 3.2. Mandatory `Summary.txt` Content Draft
```text
TITLE: Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures
AUTHORS: [Author List to be populated upon user provisioning]
VENUE: IEEE Robotics and Automation Letters (RA-L)

PAPER ABSTRACT:
Policy recovery from execution-induced failures is frequently assumed to require temporal history. However, evaluating history dependence by comparing reactive and recurrent policies conflates history access with state divergence following a failure. We introduce a paired replay-injection evaluation that isolates the causal effect of history by initializing policies at identical physical states (D <= 1e-10 m) under matched failure conditions across planar manipulation tasks in MuJoCo. In a confirmatory benchmark of 20,000 rollouts across 200 matched scenarios, recovery-augmented recurrent policies exhibit substantial motor action divergence and transient trajectory separation. However, binary recovery success exhibits no statistically significant causal-history advantage after Holm-Bonferroni correction (p_adj >= 0.2500 across all policies; negative control discordance = 0/200, 95% CI [0.00%, 1.83%]). Physical contact analysis reveals that normal contact forces and Coulomb friction act as an information-destroying bottleneck, attenuating recurrent divergence prior to terminal goal dwell.

VIDEO DESCRIPTION:
The accompanying video (video/causal_history_recovery_demo.mp4) demonstrates:
1. Off-center contact slip failure during planar object manipulation.
2. Replay-injection matched-state restoration achieving sub-atomic physical state equivalence (D <= 1e-10 m).
3. Recurrent policy action divergence upon recovery initiation.
4. Contact force damping and Coulomb friction surface attenuation leading to terminal recovery parity.
```

### 3.3. Mandatory `ReadMe.txt` Content Draft
```text
================================================================================
IEEE RA-L MULTIMEDIA PACKAGE: CAUSAL-HISTORY ROBOT POLICY RECOVERY
================================================================================

PACKAGE OVERVIEW:
This multimedia archive contains the standalone source code, pre-trained policy
checkpoints, representative benchmark manifests, and video demonstration
accompanying the paper "Causal-History Dependence in Robot Policy Recovery: A
Matched-State Evaluation under Execution-Induced Failures".

CONTENTS:
  - video/causal_history_recovery_demo.mp4 : Demonstration video (MP4, 1080p)
  - code/src/                              : Complete Python package source code
  - code/models/checkpoints/               : 4 PyTorch checkpoints (.pt)
  - code/smoke_test.py                     : Standalone verification smoke test
  - code/environment.yml                   : Conda environment specification
  - code/Dockerfile                        : Docker container specification
  - data/                                  : Representative scenario manifests

REPRODUCTION INSTRUCTIONS:
1. Environment Setup (Conda):
   conda env create -f code/environment.yml
   conda activate causal-history-recovery

2. Run Automated Verification Smoke Test:
   python code/smoke_test.py
   (Expected runtime: ~2.7s; verifies state matching residual D <= 1e-10 m)

HARDWARE REQUIREMENTS:
Standard x86-64 workstation (CPU execution supported; GPU optional).
Python 3.11, PyTorch >= 2.0, Gymnasium >= 1.0, MuJoCo >= 3.0.
```

---

## 4. Size Budget Accounting

| Item | Uncompressed Size | Compressed Size in ZIP | Budget Limit | Status |
|---|---|---|---|---|
| Video (`causal_history_recovery_demo.mp4`) | ~24.0 MB | ~23.5 MB | 45.0 MB | **PASS (`Planned`)** |
| Code & Scripts (`code/src/`, `smoke_test.py`) | ~0.4 MB | ~0.1 MB | 2.0 MB | **PASS (`Verified`)** |
| Policy Checkpoints (`models/checkpoints/*.pt`) | ~0.7 MB | ~0.6 MB | 2.0 MB | **PASS (`Verified`)** |
| Benchmark Data (`data/*.json`) | ~0.5 MB | ~0.1 MB | 2.0 MB | **PASS (`Verified`)** |
| Metadata (`ReadMe.txt`, `Summary.txt`) | ~6 KB | ~2 KB | 0.1 MB | **PASS (`Planned`)** |
| **Total Archive Size** | **~25.6 MB** | **~24.3 MB** | **50.0 MB** | **PASS ($\le 50\text{ MB}$)** |

