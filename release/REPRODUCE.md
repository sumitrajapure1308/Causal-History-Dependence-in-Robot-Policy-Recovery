# Reproduction Guide: Stage C Confirmatory Benchmark

This guide documents the exact workflow to reproduce the analysis, figures, tables, and test suites.

## 1. Quick Verification (Smoke Test)
```bash
python scripts/run_smoke_test.py
```
- Validates 4 scenarios across all 4 factorial cells.
- Evaluates reactive MLP, nominal GRU, recovery-augmented MLP, recovery-augmented GRU, and privileged oracle.
- Validates exact state matching ($D \le 10^{-10}$) and bitwise determinism ($D = 0.0$).
- Runtime: ~2.5 seconds.

## 2. Test Suite Execution
```bash
pytest tests -v
```
- Executes 67 automated unit and integration tests.
- 100% pass rate in ~12 seconds.

## 3. Re-Running Confirmatory Analysis
```bash
python scripts/analyze_stage_c_benchmark.py
```
- Inputs: `results/phase_12_stage_c/rollouts/rollout_records.jsonl` (20,000 records).
- Computes McNemar exact tests, Wilcoxon signed-rank tests, Holm-Bonferroni corrections, and Clopper-Pearson confidence intervals.
- Generates reports in `results/phase_12_stage_c/analysis/`.

## 4. Re-Generating Paper Figures (600 DPI)
```bash
python scripts/make_paper_figures.py
```
- Outputs: 14 publication figures in PNG and vector PDF under `figures/benchmark/paper/`.

## 5. Executing Verification Notebooks
All 62 notebooks in `notebooks/` are pre-executed with visible cell outputs:
- Notebooks 48–56: Phase 12 Stage C confirmatory benchmark analysis.
- Notebooks 57–61: Phase 13 evidence package and robustness audits.
- Notebook 62: Phase 15 final reproducibility audit.
