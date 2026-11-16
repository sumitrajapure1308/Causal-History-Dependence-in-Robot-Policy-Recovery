## Table 7: Benchmark Reproducibility and Data Provenance Audit Checklist
*Data Source: `results/phase_12_stage_c/phase_12_file_hashes.json`*

| Verification Item | Status | Lineage & Validation Evidence |
| :--- | :---: | :--- |
| **Deterministic Simulation Stepping** | `VERIFIED` | 100% determinism passing in `tests/test_determinism.py` |
| **Bitwise State Matching** | `VERIFIED` | Exact state matching ($D \le 10^{-10}$) across 200 scenarios |
| **Disjoint Seed Schedule** | `VERIFIED` | Scenario seeds $\ge 10000$; Evaluation seeds `15001`–`15005` |
| **Pseudoreplication Avoidance** | `VERIFIED` | Scenario-level inference unit ($N=200$); replicate seeds averaged |
| **Cryptographic Hash Lineage** | `VERIFIED` | 310 artifact SHA-256 signatures in `phase_12_file_hashes.json` |
| **Automated Test Suite** | `VERIFIED` | 67 / 67 pytest tests passing in 18.92s |
