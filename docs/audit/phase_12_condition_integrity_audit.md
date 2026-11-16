# Phase 12 Condition Integrity Audit

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 12 (Official Confirmatory Stage C Benchmark Execution)  
**Status:** `VERIFIED`  

## 1. History-Intervention Condition Census
| Condition | Description | Rollouts Recorded | Expected | Balance Status |
| :--- | :--- | :---: | :---: | :---: |
| **B0** | Full unrolled memory prefix | 4000 | 4,000 | `PASS` |
| **B1** | Action history masked | 4000 | 4,000 | `PASS` |
| **B2** | Observation history masked | 4000 | 4,000 | `PASS` |
| **B3** | Full observation + action masked | 4000 | 4,000 | `PASS` |
| **B4** | Direct matched injection (memoryless) | 4000 | 4,000 | `PASS` |

## 2. Counterfactual Intervention Semantics Audit
- **B0 Unrolled Sequence Length:** Mean = 17.4 steps ($> 1$).
- **B4 Injected Observation Length:** Exactly 1 current step ($= 1.0$).
- **Bitwise State Matching:** Injected initial physical states across B0–B4 verify exact state equivalence ($D \le 10^-10$).
- **Policy Recurrent Reset:** Verified clean hidden state zeroing before unrolling or direct injection.
- **Negative Control Invariance:** Memoryless MLP policies verified strictly invariant to observation masking.

**Audit Verdict:** `PASSED (100% CONDITION INTEGRITY)`
