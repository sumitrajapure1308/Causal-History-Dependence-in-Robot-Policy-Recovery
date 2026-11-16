# Phase 12 Reproducibility Audit

**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 12 (Official Confirmatory Stage C Benchmark Execution)  
**Status:** `VERIFIED & REPRODUCIBLE`  

## 1. System Environment & Toolchain
- **OS Platform:** Windows-10-10.0.26300-SP0
- **Python Version:** 3.11.0
- **MuJoCo Version:** 3.10.0
- **PyTorch Version:** 2.13.0+cpu
- **NumPy Version:** 2.4.6
- **Version Control:** Local Git not initialized; audit secured via cryptographic SHA-256 signatures.

## 2. Checkpoint Provenance Hashes
| Checkpoint Path | Architecture | SHA-256 Digest |
| :--- | :--- | :--- |
| `reactive_mlp_best.pt` | Reactive MLP | `f99beb840b878d34...` |
| `history_gru_best.pt` | History-Aware GRU | `5fcf94e2410efca8...` |
| `recovery_augmented_mlp_seed42.pt` | Rec-Aug MLP | `1aba926f4ad7bbd1...` |
| `recovery_augmented_gru_seed456.pt` | Rec-Aug GRU | `7888cc1fc63b7d2d...` |

## 3. Benchmark Execution Data Signatures
- **Benchmark Script:** `scripts/run_stage_c_benchmark.py` (`1c846ab0704570f3...`)
- **Rollout Output File:** `rollout_records.jsonl`
- **Output SHA-256:** `d8a2c8dbc88586d938d7086450bc50099511b2f4aa057dd617d33662a6bd3cea`
- **Output File Size:** 24.86 MB
- **Evaluation Seeds:** `[15001, 15002, 15003, 15004, 15005]`

**Audit Verdict:** `PASSED (FULL REPRODUCIBILITY SECURED)`
