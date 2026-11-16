# History Information Provenance and Policy Input Specification

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Status:** VALIDATED SPECIFICATION  
**Document:** `docs/methodology/history_information_provenance.md`  
**Date:** 2026-11-09  

---

## 1. Overview and Rationale

A foundational requirement in causal-history auditing is knowing exactly what information each policy architecture receives at every inference step. In robot policy evaluation, history-dependence is frequently conflated with architectural recurrence (e.g., whether a policy uses a GRU or Transformer). However, if a non-recurrent feedforward policy (MLP) receives input features that are themselves temporal summaries, counters, or latching failure flags computed from past observations, **that policy is not memoryless with respect to physical history**.

This document maps the complete information provenance for all twelve input channels across all four evaluated policy architectures, audits online vs. privileged access, and defines the precise scope of counterfactual history interventions.

---

## 2. Comprehensive Input Provenance Table

| # | Input Field / Channel | Dimensionality | Data Source | Online Availability | Privileged Status | Derived from Past History? | Condition B0 (Preserved) | Condition B4 (History Removed) |
|---|---|---|---|---|---|---|---|---|
| 1 | **Current Physical Observation ($o_t$)** | 20 | Pusher EE pose (3), cube pos (3), cube rot (4), relative pos (3), task goal (3), velocities (4) | Online (sensors / FK) | Unprivileged | **No** (Instantaneous physical state) | Preserved | Preserved (Exact matched state) |
| 2 | **Observation History Buffer ($o_{t-k:t}$)** | $k \times 20$ (e.g. $10 \times 20$) | Rolling FIFO queue of past environment observations | Online (cached) | Unprivileged | **Yes** (Sequence of past observations) | Preserved / Replayed | Zeroed or padded with $o_t$ |
| 3 | **Previous Action ($a_{t-1}$)** | 3 | Rolling buffer of past executed robot command deltas | Online (cached) | Unprivileged | **Yes** (Previous motor command) | Preserved / Replayed | Zero-masked ($[0,0,0]$) |
| 4 | **Contact History ($c_{t-k:t}$)** | $k \times 1$ | Rolling buffer of binary cube-pusher contact indicators | Online (sensor) | Unprivileged | **Yes** (Past contact sequence) | Preserved / Replayed | Zero-masked ($0.0$) |
| 5 | **Recurrent Hidden State ($h_t$)** | 128 | Internal hidden activations of GRU layer | Online (internal) | Unprivileged | **Yes** (Recursive integration of history) | Reconstructed via prefix unroll | Reset to zero ($\mathbf{0}_{128}$) |
| 6 | **Failure Detection Flag ($f_t$)** | 1 | Latching boolean indicator ($1.0$ if $|\text{yaw}| > 15^\circ$ or drift $> 2.5\text{ cm}$) | Online (computed) | Unprivileged | **Yes** (Latching latch remembers past threshold crossing) | Preserved | Recomputed from current $o_t$ |
| 7 | **Deviation Duration ($\tau_{\text{dev}}$)** | 1 | Normalized elapsed time counter: $(t - t_{\text{dev}}) / 100$ | Online (internal counter) | Unprivileged | **Yes** (Explicit temporal history duration) | Preserved | Recomputed from current $o_t$ ($0.0$ at injection) |
| 8 | **Deviation Magnitude ($\delta_{\text{dev}}$)** | 1 | Instantaneous yaw deviation magnitude recorded at detection | Online (computed) | Unprivileged | **Partially** (Reflects state at deviation step) | Preserved | Evaluated on current state |
| 9 | **Remaining Horizon ($H_{\text{rem}}$)** | 1 | Normalized steps remaining: $(T_{\text{max}} - t) / 150$ | Online (task spec) | Unprivileged | **No** (Task parameter supplied to agent) | Preserved | Preserved |
| 10 | **Task Goal Position ($g$)** | 3 | Target Cartesian position coordinates $(x, y, z)$ | Online (task spec) | Unprivileged | **No** (Static task parameter) | Preserved | Preserved |
| 11 | **Observation Normalization** | N/A | Fixed offline scale bounds / clipping limits | Offline static | Unprivileged | **No** (Static model parameter) | Preserved | Preserved |
| 12 | **Controller Step Counter ($t$)** | 1 | Internal integer step counter | Online (internal) | Unprivileged | **Yes** (Counts total steps elapsed) | Preserved ($t = t_{\text{dev}}$) | Reset to 0 |

---

## 3. Architecture-Specific Input Breakdown

### 1. Reactive MLP (`reactive_mlp`):
- **Input Dimensions:** 20
- **Channels Consumed:** Field 1 only ($o_t$).
- **Memory Assessment:** **Strictly memoryless**. At any step $t$, the action $a_t = \pi(o_t)$ depends exclusively on the instantaneous physical state. It has zero capacity to store or process history.

### 2. History-Aware GRU (`history_gru`):
- **Input Dimensions:** 23 ($o_t \in \mathbb{R}^{20}$ concatenated with $a_{t-1} \in \mathbb{R}^3$).
- **Channels Consumed:** Fields 1, 3, and internal Field 5 ($h_t$).
- **Memory Assessment:** **Recurrent memory architecture**. Temporal dependence is mediated entirely through the recurrent hidden state $h_t$ and the explicit 1-step previous action feedback.

### 3. Recovery-Augmented MLP (`recovery_augmented_mlp`):
- **Input Dimensions:** 24 ($o_t \in \mathbb{R}^{20}$, failure flag $\in \mathbb{R}^1$, deviation duration $\in \mathbb{R}^1$, deviation magnitude $\in \mathbb{R}^1$, remaining horizon $\in \mathbb{R}^1$).
- **Channels Consumed:** Fields 1, 6, 7, 8, 9, 12.
- **Memory Assessment:** **Non-recurrent architecture with temporal features**. Although the network itself has no recurrent weights ($h_t = \emptyset$), it consumes `deviation_duration` and `failure_flag`. When evaluated online, `deviation_duration` tracks how many steps have elapsed since the failure threshold was triggered. Therefore, **this policy is not memoryless with respect to physical history**.

### 4. Recovery-Augmented GRU (`recovery_augmented_gru`):
- **Input Dimensions:** 28 (Augmented observation 24, previous action 3, contact indicator 1).
- **Channels Consumed:** Fields 1, 3, 4, 5, 6, 7, 8, 9, 12.
- **Memory Assessment:** **Full dual memory**. Integrates both explicit temporal indicators in the observation vector and latent recurrent memory in $h_t$.

---

## 4. Redefining Intervention Scope: B0 through B4

To eliminate ambiguity in causal claims, the definitions of conditions B0–B4 are formalized below:

### Legacy vs. Corrected Definitions:

- **Condition B0 (Full Preserved History):**
  - *Legacy Definition:* "Full history preserved."
  - *Corrected Definition:* **Policy-specific memory reconstructed via prefix unrolling**. The policy's internal recurrent state $h(t_{\text{dev}})$ and historical buffers are unrolled by stepping through the exact recorded sequence of observations and actions up to deviation step $t_{\text{dev}}$.

- **Condition B1 (Action History Masked):**
  - *Legacy Definition:* "Action history removed."
  - *Corrected Definition:* **Explicit action-channel zeroing with intact recurrent state**. The explicit input $a_{t-1}$ is zeroed, but latent memory in $h(t)$ remains unablated.

- **Condition B2 (Observation History Window Masked):**
  - *Legacy Definition:* "Observation history removed."
  - *Corrected Definition:* **Observation buffer replaced with current state repeat; recurrent state intact**.

- **Condition B3 (Hidden State Reset):**
  - *Legacy Definition:* "Recurrent memory reset."
  - *Corrected Definition:* **Recurrent state zeroed ($h = \mathbf{0}$) with explicit buffers intact**.

- **Condition B4 (Direct Matched-State Injection / Memory Removed):**
  - *Legacy Definition:* "All history removed."
  - *Corrected Definition:* **Direct physical state injection with zeroed recurrent memory and zeroed explicit buffers**. The policy starts cold at the matched physical state ($h = \mathbf{0}$, $a_{\text{prev}} = \mathbf{0}$, buffers filled with $o_{\text{dev}}$).
  - *Critical Caveat:* For `recovery_augmented_mlp` and `recovery_augmented_gru`, if the failure flag and deviation magnitude are computed from the current physical observation, they reflect current physical deviation, while `deviation_duration` is initialized to $0.0$. Thus, B4 eliminates past duration and recurrent memory, but retains instantaneous physical deviation indicators.

---

## 5. Methodological Guidelines for Causal Attribution

1. **Explicit vs. Latent Channels:** One cannot claim to have isolated the "effect of action history" by zeroing the input token $a_{t-1}$ if the recurrent state $h_t$ already heavily encodes the past action trajectory. B1 is strictly an explicit-input ablation, not an information-theoretic erasure of action history.
2. **True Memoryless Baseline:** Only `reactive_mlp` represents a mathematically memoryless control policy.

