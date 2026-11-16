#!/usr/bin/env python3
"""
Build Phase 15 Submission Release Package:
Generates all 23 release package files in release/
"""

import os
import sys
import json
import hashlib
import glob

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
release_dir = os.path.join(repo_root, 'release')
os.makedirs(release_dir, exist_ok=True)

def get_file_sha256(path):
    if not os.path.isfile(path):
        return "MISSING"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

print(f"Building Release Package in {release_dir}...")

# 1. LICENSE (MIT License)
license_text = """MIT License

Copyright (c) 2026 Causal-History Policy Recovery Research Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
with open(os.path.join(release_dir, 'LICENSE'), 'w', encoding='utf-8') as f:
    f.write(license_text.strip() + '\n')

# 2. CITATION.cff
citation_cff = """cff-version: 1.2.0
message: "If you use this benchmark, code, or data, please cite it as below."
title: "Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures"
authors:
  - family-names: "Research Contributors"
    given-names: "Causal-History Recovery"
version: 1.0.0-rc1
date-released: 2026-11-10
url: "https://github.com/causal-history-recovery/causal-history-recovery"
license: MIT
keywords:
  - "robot learning"
  - "policy recovery"
  - "causal history"
  - "counterfactual evaluation"
  - "matched state"
  - "contact manipulation"
preferred-citation:
  type: article
  title: "Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures"
  authors:
    - family-names: "Research Contributors"
      given-names: "Causal-History Recovery"
  journal: "Robotics Science and Systems (Archival Draft)"
  year: 2026
"""
with open(os.path.join(release_dir, 'CITATION.cff'), 'w', encoding='utf-8') as f:
    f.write(citation_cff.strip() + '\n')

# 3. requirements.txt
requirements_txt = """gymnasium>=0.29.0,<=1.3.0
torch>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
pyyaml>=6.0
pytest>=7.3.0
nbclient>=0.7.0
nbformat>=5.9.0
ipykernel>=6.20.0
"""
with open(os.path.join(release_dir, 'requirements.txt'), 'w', encoding='utf-8') as f:
    f.write(requirements_txt.strip() + '\n')

# 4. environment.yml
environment_yml = """name: causal-history-recovery
channels:
  - pytorch
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pytorch
  - torchvision
  - cpuonly
  - numpy>=1.24.0
  - scipy>=1.10.0
  - matplotlib>=3.7.0
  - pyyaml>=6.0
  - pytest>=7.3.0
  - pip
  - pip:
      - gymnasium>=0.29.0
      - nbclient>=0.7.0
      - nbformat>=5.9.0
      - ipykernel>=6.20.0
"""
with open(os.path.join(release_dir, 'environment.yml'), 'w', encoding='utf-8') as f:
    f.write(environment_yml.strip() + '\n')

# 5. pyproject.toml
pyproject_toml = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "causal-history-recovery"
version = "1.0.0-rc1"
description = "Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures"
readme = "README.md"
authors = [{ name = "Causal History Recovery Contributors" }]
license = { text = "MIT" }
requires-python = ">=3.10"
dependencies = [
    "gymnasium>=0.29.0",
    "torch>=2.0.0",
    "numpy>=1.24.0",
    "scipy>=1.10.0",
    "matplotlib>=3.7.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.3.0",
    "nbclient>=0.7.0",
    "nbformat>=5.9.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
"""
with open(os.path.join(release_dir, 'pyproject.toml'), 'w', encoding='utf-8') as f:
    f.write(pyproject_toml.strip() + '\n')

# 6. Dockerfile
dockerfile = """# Submission Reproducibility Dockerfile
FROM python:3.11-slim

LABEL maintainer="Causal History Recovery Contributors"
LABEL description="Matched-State Causal-History Evaluation of Robot Policy Recovery"
LABEL version="1.0.0-rc1"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace/src

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    git \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libosmesa6-dev \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY release/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /workspace/src/
COPY models/ /workspace/models/
COPY configs/ /workspace/configs/
COPY results/ /workspace/results/
COPY tests/ /workspace/tests/
COPY scripts/ /workspace/scripts/

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD python -c "import causal_history_recovery; import torch; import gymnasium" || exit 1

ENTRYPOINT ["python"]
CMD ["scripts/run_smoke_test.py"]
"""
with open(os.path.join(release_dir, 'Dockerfile'), 'w', encoding='utf-8') as f:
    f.write(dockerfile.strip() + '\n')

# 7. docker-compose.yml
docker_compose = """version: '3.8'

services:
  reproducibility-benchmark:
    build:
      context: ..
      dockerfile: release/Dockerfile
    container_name: causal_history_recovery_reproduce
    volumes:
      - ../results:/workspace/results
      - ../figures:/workspace/figures
    command: python scripts/run_smoke_test.py
    environment:
      - PYTHONUNBUFFERED=1
"""
with open(os.path.join(release_dir, 'docker-compose.yml'), 'w', encoding='utf-8') as f:
    f.write(docker_compose.strip() + '\n')

# 8. .gitignore & .dockerignore
gitignore_text = """__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.ipynb_checkpoints/
*.egg-info/
dist/
build/
.env
"""
with open(os.path.join(release_dir, '.gitignore'), 'w', encoding='utf-8') as f:
    f.write(gitignore_text.strip() + '\n')
with open(os.path.join(release_dir, '.dockerignore'), 'w', encoding='utf-8') as f:
    f.write(gitignore_text.strip() + '\n')

# 9. smoke_test.py (copy of scripts/run_smoke_test.py)
with open(os.path.join(repo_root, 'scripts', 'run_smoke_test.py'), 'r', encoding='utf-8') as f:
    smoke_py_content = f.read()
with open(os.path.join(release_dir, 'smoke_test.py'), 'w', encoding='utf-8') as f:
    f.write(smoke_py_content)

# 10. smoke_test.sh
smoke_sh = """#!/usr/bin/env bash
set -e
echo "Running Causal-History Recovery Submission Smoke Test..."
python scripts/run_smoke_test.py
pytest tests -v
echo "Smoke test passed successfully."
"""
with open(os.path.join(release_dir, 'smoke_test.sh'), 'w', encoding='utf-8') as f:
    f.write(smoke_sh.strip() + '\n')

# 11. run_all.py
run_all_py = """#!/usr/bin/env python3
\"\"\"Full Benchmark Reproduction Entrypoint.\"\"\"
import os
import sys
import subprocess

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

print("=== 1. Running Unit & Integration Tests ===")
ret = subprocess.run([sys.executable, "-m", "pytest", os.path.join(repo_root, "tests"), "-v"])
if ret.returncode != 0:
    sys.exit(ret.returncode)

print("\\n=== 2. Running Submission Smoke Test ===")
ret = subprocess.run([sys.executable, os.path.join(repo_root, "scripts", "run_smoke_test.py")])
if ret.returncode != 0:
    sys.exit(ret.returncode)

print("\\n=== Full Verification Complete: ALL TESTS PASSED ===")
"""
with open(os.path.join(release_dir, 'run_all.py'), 'w', encoding='utf-8') as f:
    f.write(run_all_py.strip() + '\n')

# 12. run_all.sh
run_all_sh = """#!/usr/bin/env bash
set -e
python release/run_all.py
"""
with open(os.path.join(release_dir, 'run_all.sh'), 'w', encoding='utf-8') as f:
    f.write(run_all_sh.strip() + '\n')

# 13. INSTALL.md
install_md = """# Installation Guide: Causal-History Policy Recovery Benchmark

## Prerequisites
- Operating System: Linux (Ubuntu 20.04/22.04), macOS, or Windows 10/11 (x86_64)
- Python: Version 3.10 or 3.11
- Minimum Hardware: 4 CPU cores, 8 GB RAM, 2 GB free disk space

## Option 1: Conda Environment (Recommended)
```bash
conda env create -f release/environment.yml
conda activate causal-history-recovery
pip install -e .
```

## Option 2: Virtualenv & Pip
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
pip install --upgrade pip
pip install -r release/requirements.txt
pip install -e .
```

## Option 3: Docker
```bash
docker build -t causal-history-recovery:latest -f release/Dockerfile .
docker run --rm causal-history-recovery:latest
```

## Verify Installation
```bash
python scripts/run_smoke_test.py
pytest tests -v
```
Expected output: 67 passed tests in ~12s.
"""
with open(os.path.join(release_dir, 'INSTALL.md'), 'w', encoding='utf-8') as f:
    f.write(install_md.strip() + '\n')

# 14. REPRODUCE.md
reproduce_md = """# Reproduction Guide: Stage C Confirmatory Benchmark

This guide documents the exact workflow to reproduce the analysis, figures, tables, and test suites.

## 1. Quick Verification (Smoke Test)
```bash
python scripts/run_smoke_test.py
```
- Validates 4 scenarios across all 4 factorial cells.
- Evaluates reactive MLP, nominal GRU, recovery-augmented MLP, recovery-augmented GRU, and privileged oracle.
- Validates exact state matching ($D \\le 10^{-10}$) and bitwise determinism ($D = 0.0$).
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
"""
with open(os.path.join(release_dir, 'REPRODUCE.md'), 'w', encoding='utf-8') as f:
    f.write(reproduce_md.strip() + '\n')

# 15. DATA.md
data_md = """# Data Management & Provenance Specification

## Primary Benchmark Data
- **Location:** `results/phase_12_stage_c/rollouts/rollout_records.jsonl`
- **Volume:** Exactly 20,000 JSONL records ($15.5\\text{ MB}$).
- **Structure:** Balanced $2 \\times 2 \\times 4 \\times 5 \\times 5 \\times 50$ factorial design.
  - Tasks (2): `task1_cube`, `task2_puck`
  - Failure Modes (2): `rotational_slip`, `contact_loss`
  - Policies (4): `reactive_mlp`, `history_gru`, `recovery_augmented_mlp`, `recovery_augmented_gru`
  - Conditions (5): $B_0, B_1, B_2, B_3, B_4$
  - Replicate Seeds (5): `15001, 15002, 15003, 15004, 15005`
  - Scenarios (200): 50 per cell (Disjoint seeds $\\ge 10000$)

## Scenario Manifest
- **Location:** `results/phase_12_stage_c/scenario_manifest.json`
- **Contents:** Exact failure snapshots, yaw deviations, lateral drifts, and privileged oracle recoverability audit.

## Data Lineage & Immutability Rules
Raw rollout data (`results/phase_12_stage_c/rollouts/`) is strictly immutable. All analysis scripts read directly from these JSONL records without altering source data.
"""
with open(os.path.join(release_dir, 'DATA.md'), 'w', encoding='utf-8') as f:
    f.write(data_md.strip() + '\n')

# 16. CODE.md
code_md = """# Codebase Architecture & Modular Organization

The source code is structured as an installable Python package under `src/causal_history_recovery/`:

```
src/causal_history_recovery/
├── environments/               # MuJoCo/Gymnasium simulation environments
│   ├── push_target_env.py      # Task 1: Cube pushing with Coulomb friction
│   ├── second_push_task_env.py # Task 2: Puck pushing with altered mass and friction
│   ├── state_snapshot.py       # Lossless bitwise state capture and restore
│   └── assets/                 # MuJoCo XML physical model definitions
├── policies/                   # Policy architectures and registry
│   ├── reactive_mlp.py         # 2-layer MLP baseline (negative control)
│   ├── history_gru.py          # 1-layer GRU baseline
│   ├── recovery_augmented_mlp.py # Recovery-trained MLP
│   ├── recovery_augmented_gru.py # Recovery-trained GRU
│   └── policy_registry.py      # Unified factory and checkpoint loader
├── controllers/
│   └── privileged_oracle.py    # State-feedback reachability verifier
├── counterfactuals/
│   └── paired_scenario_generator.py # Scenario mining and failure trigger
├── matching/
│   └── state_matcher.py        # Composite distance and verification
├── metrics/
│   ├── history_dependence.py   # History dependence calculation
│   └── outcome_hierarchy.py    # 4-tier outcome categorization
└── rollout/
    ├── episode_logger.py       # Structured JSONL logging
    └── rollout_collector.py    # Batch rollout runner
```
"""
with open(os.path.join(release_dir, 'CODE.md'), 'w', encoding='utf-8') as f:
    f.write(code_md.strip() + '\n')

# 17. CHECKPOINTS.md
checkpoints_md = """# Policy Checkpoints Specification

Pre-trained model checkpoints are stored in `models/checkpoints/`:

| Checkpoint Name | Policy Architecture | Hidden Dims | Input Dim | Output Dim | Parameters | Training Dataset | Primary Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `reactive_mlp_best.pt` | 2-layer MLP | 64 | 10 | 2 | ~5,000 | Nominal demonstrations | Negative Control |
| `history_gru_best.pt` | 1-layer GRU | 64 | 10 | 2 | ~17,000 | Nominal demonstrations | Nominal Recurrent Baseline |
| `recovery_augmented_mlp_best.pt` | 2-layer MLP | 64 | 10 | 2 | ~5,000 | Augmented recovery dataset | Recovery-Trained Memoryless |
| `recovery_augmented_gru_best.pt` | 1-layer GRU | 64 | 10 | 2 | ~17,000 | Augmented recovery dataset | Recovery-Trained Recurrent |

All checkpoints load seamlessly via `load_policy(path)` and run on standard CPU architecture.
"""
with open(os.path.join(release_dir, 'CHECKPOINTS.md'), 'w', encoding='utf-8') as f:
    f.write(checkpoints_md.strip() + '\n')

# 18. FIGURES.md
figures_md = """# Publication Figures Catalog

All 14 publication paper figures are stored in `figures/benchmark/paper/` and mirrored in `docs/manuscript/figures/`:
- Formats: High-resolution PNG (600 DPI) and scalable vector PDF.
- Figures 1–14 cover:
  1. Methodological pipeline: Paired Replay-Injection Matching.
  2. Scenario generation and yaw/drift distributions.
  3. Bitwise state-matching distance ($D \\le 10^{-10}\\text{ m}$).
  4. Recovery success rates across conditions $B_0–B_4$.
  5. Primary binary recovery comparison ($B_0$ vs $B_4$).
  6. Task-stratified recovery (Task 1 vs Task 2).
  7. Failure-mode stratified recovery (Rotational slip vs Contact loss).
  8. History-dependence score $H_R$.
  9. Continuous goal error paired difference distribution $\\Delta e$.
  10. Forest plot of 95% bootstrap confidence intervals.
  11. Mechanism diagnostics (Hidden state norm, action divergence, path divergence).
  12. Recovery failure mode decomposition ($M_1–M_6$).
  13. Policy ranking invariance (Kendall's $\\tau = 0.3333$).
  14. Multi-dimensional sensitivity analysis (14 dimensions).
"""
with open(os.path.join(release_dir, 'FIGURES.md'), 'w', encoding='utf-8') as f:
    f.write(figures_md.strip() + '\n')

# 19. TABLES.md
tables_md = """# Publication Tables Catalog

All 7 publication tables are stored in `docs/manuscript/tables/`:
- `table_01.md`: Methodological comparison with RoboRecover, LIBERO-Recover, and LIBERO-Pro2.0.
- `table_02.md`: Factorial experimental design matrix ($20,000$ rollouts).
- `table_03.md`: Admitted scenario kinematic and disturbance statistics ($N=200$).
- `table_04.md`: Main confirmatory binary recovery results: $B_0$ vs $B_4$ McNemar exact tests.
- `table_05.md`: Continuous final goal error analysis and Wilcoxon signed-rank tests.
- `table_06.md`: Counterfactual history intervention ablations ($B_0–B_4$).
- `table_07.md`: Benchmark reproducibility and data provenance audit checklist.
"""
with open(os.path.join(release_dir, 'TABLES.md'), 'w', encoding='utf-8') as f:
    f.write(tables_md.strip() + '\n')

# 20. NOTEBOOKS.md
notebooks_md = """# Executed Jupyter Notebooks Catalog

The repository includes 62 Jupyter notebooks in `notebooks/`, all pre-executed with complete cell outputs:
- `01–10`: Environment prototyping and dynamics audits (Phases 1–2).
- `11–20`: Policy suite implementation and nominal baseline training (Phases 3–4).
- `21–30`: Paired scenario generation and failure mining (Phases 5–6).
- `31–40`: State-matching and history-intervention validity diagnostics (Phases 7–8).
- `41–47`: Held-out scenario generation and staged pilot confirmation (Phases 9–11).
- `48–56`: Phase 12 Stage C confirmatory benchmark execution and pre-registered statistical analysis.
- `57–61`: Phase 13 evidence synthesis, null audits, and multi-dimensional robustness.
- `62`: Phase 15 final reproducibility audit and end-to-end smoke-test verification.
"""
with open(os.path.join(release_dir, 'NOTEBOOKS.md'), 'w', encoding='utf-8') as f:
    f.write(notebooks_md.strip() + '\n')

# 21. README.md
readme_md = """# Matched-State Causal-History Evaluation of Robot Policy Recovery under Execution-Induced Failures

**Status:** `Release Candidate`, `Submission-Ready Evidence`, `Pre-Registered`, `Confirmatory`  
**License:** MIT License  
**Repository Root:** `causal-history-recovery/`  

---

## Abstract & Research Core

Autonomous robot manipulation policies frequently experience execution failures caused by kinematic slips and contact disruptions during contact-rich tasks. Standard recovery benchmarks evaluate failure behaviors by restarting executions or replaying trajectories, thereby confounding the instantaneous physical state with the preceding execution history. We formulate a matched-state causal-history evaluation protocol that decouples physical state from execution history using bitwise simulator snapshots with residual matching error below 1e-10. Across two planar pushing manipulation tasks and two distinct execution failure modes (rotational slip and contact loss), 200 recoverable scenarios were mined and verified under privileged oracle reachability. Four policy architectures—reactive MLP, nominal GRU, recovery-augmented MLP, and recovery-augmented GRU—were systematically evaluated across five counterfactual intervention history conditions (B0 to B4) spanning 20,000 confirmatory rollouts. Under the tested policies, tasks, and matched-state protocol, binary recovery success and final goal error were history-invariant, although preserved recurrent history changed immediate control behavior and object trajectories. Paired scenario-level McNemar exact tests confirmed no statistically significant binary advantage for preserved history over direct matched injection across all policy architectures (adjusted p >= 0.2500). Continuous final goal distance errors exhibited negligible differences (adjusted p = 1.0000, Cohen's d <= 0.137). Mechanism diagnostics revealed that recurrent unrolling reconstructed internal representations and induced immediate action divergence (0.0038 m/step) and trajectory divergence (2.48 cm); however, downstream Coulomb friction and normal contact constraints attenuated this kinematic variance before the terminal goal basin. The results are simulation-based and strictly limited to the tested settings. Complete open-source code, checkpoints, seeds, and cryptographic manifests ensure complete scientific reproducibility.

---

## Core Research Question
“When physically equivalent failure states are reached through different execution histories, do robot policies exhibit different detection, diagnosis, recovery, and final task-completion performance?”

## Main Contribution
“A matched-state causal-history evaluation protocol that compares preserved execution history, prefix replay, and physically matched state injection under controlled conditions.”

---

## Quickstart & Verification

```bash
# 1. Install dependencies
pip install -r release/requirements.txt
pip install -e .

# 2. Run automated smoke test
python scripts/run_smoke_test.py

# 3. Run complete test suite (67 tests)
pytest tests -v
```

---

## Limitations
“The results are simulation-based and limited to the tested tasks, policies, failure modes, and matched-state protocol; they do not establish real-robot validity or generalization beyond these conditions.”

---

## Disclosures & Statements
- **Ethical Considerations:** Simulation-only robotics research without human or animal subjects.
- **Conflict of Interest:** The authors declare no competing financial or personal interests.
- **Funding:** Conducted as an independent robotics research project.
- **Data Availability:** Complete 20,000 rollout records are available in `results/phase_12_stage_c/rollouts/`.
- **Code Availability:** All source code, configs, notebooks, and models are open-source under the MIT License.
"""
with open(os.path.join(release_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_md.strip() + '\n')

# 22. manifest.json
manuscript_hash = get_file_sha256(os.path.join(repo_root, 'docs', 'manuscript', 'draft', 'manuscript.md'))
data_hash = get_file_sha256(os.path.join(repo_root, 'results', 'phase_12_stage_c', 'rollouts', 'rollout_records.jsonl'))
cfg_hash = get_file_sha256(os.path.join(repo_root, 'configs', 'evaluation', 'stage_c_benchmark.yaml'))
scen_hash = get_file_sha256(os.path.join(repo_root, 'results', 'phase_12_stage_c', 'scenario_manifest.json'))
smoke_hash = get_file_sha256(os.path.join(repo_root, 'scripts', 'run_smoke_test.py'))
license_hash = get_file_sha256(os.path.join(release_dir, 'LICENSE'))
citation_hash = get_file_sha256(os.path.join(release_dir, 'CITATION.cff'))

release_files = glob.glob(os.path.join(release_dir, '*'))
total_release_size = sum(os.path.getsize(f) for f in release_files if os.path.isfile(f))

manifest_data = {
    "release_id": "causal-history-recovery-v1.0.0-rc1",
    "release_version": "1.0.0-rc1",
    "release_date": "2026-11-10",
    "status": "Release Candidate",
    "verification_status": "Submission-Ready Evidence",
    "manuscript_sha256": manuscript_hash,
    "primary_data_sha256": data_hash,
    "scenario_manifest_sha256": scen_hash,
    "benchmark_config_sha256": cfg_hash,
    "smoke_test_script_sha256": smoke_hash,
    "license_sha256": license_hash,
    "citation_cff_sha256": citation_hash,
    "total_release_files": len(release_files),
    "total_release_size_bytes": total_release_size,
    "files": {os.path.basename(f): get_file_sha256(f) for f in release_files if os.path.isfile(f)}
}

with open(os.path.join(release_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest_data, f, indent=2)

print(f"Release package generated successfully: {len(release_files)} files created in {release_dir}.")

