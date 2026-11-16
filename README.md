# Causal-History Dependence in Robot Policy Recovery: A Matched-State Evaluation under Execution-Induced Failures

[![Code License: MIT](https://img.shields.io/badge/Code_License-MIT-yellow.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data_License-CC_BY_4.0-lightgrey.svg)](LICENSE-DATA.md)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Physics: MuJoCo](https://img.shields.io/badge/Physics-MuJoCo_3.x-red.svg)](https://mujoco.org/)

This repository hosts the official open-source evaluation suite and benchmarking framework for investigating **causal-history dependence in robot policy recovery under matched physical states**.

---

## 1. Project Overview & Methodology

Robotic manipulation policies frequently encounter execution-induced anomalies (e.g., rotational slip, contact loss). Standard benchmark evaluations conflate temporal history access with physical state divergence following a failure. 

This repository implements the **Paired Replay-Injection Matching** protocol:
- Intercepts execution at deterministic failure events ($t_{\text{fail}}$).
- Clones full simulator dynamics to matched physical precision ($D(s_1, s_2) \le 10^{-10}\text{ m}$).
- Evaluates learned reactive and recurrent policies from identical physical states under controlled counterfactual history prefixes.

### Evaluated Counterfactual History Conditions

1. **Condition B0 (Nominal Prefix Replay):** Execution begins from $t=0$ through the nominal failure prefix with uninhibited recurrent state unrolling.
2. **Condition B1 (Action History Masked):** Replayed observation trajectory with preceding action buffers clamped to zero ($a_{t-1} = 0$).
3. **Condition B2 (Observation History Ablated):** Instantaneous physical injection with history observation buffers ablated (repeat current observation).
4. **Condition B3 (Hidden-State Reset):** Full observation-action prefix replay with recurrent policy memory zeroed ($h = 0$) at $t_{\text{fail}}$.
5. **Condition B4 (Direct Matched Injection):** Direct physical injection into $s_{t_{\text{fail}}}$ with reset memory ($h = 0$) and buffers, serving as the unconfounded counterfactual comparison against B0.

---

## 2. Repository Architecture

```text
causal-history-recovery/
├── LICENSE                    <- MIT License for software and source code
├── LICENSE-DATA.md            <- CC BY 4.0 License for datasets, figures, and documentation
├── README.md                  <- This document
├── PROJECT_SCOPE.md           <- Scientific boundaries and scope specification
├── pyproject.toml             <- Python package configuration
├── requirements.txt           <- Pinned dependencies
├── configs/                   <- Configuration management
│   ├── tasks/                 <- Task definitions (push target, puck slide)
│   ├── policies/              <- Policy architectures (MLP, GRU, Recovery-Augmented)
│   ├── matching/              <- State matching distance tolerances & weights
│   ├── evaluation/            <- Evaluation protocols & suite parameters
│   └── experiments/           <- Experiment sweeps and random seeds
├── src/
│   └── causal_history_recovery/
│       ├── environments/      <- MuJoCo wrappers, failure models, & state serialization
│       ├── controllers/       <- Privileged geometric oracle filter
│       ├── policies/          <- Reactive, history-aware, and recovery-augmented policies
│       ├── counterfactuals/   <- Paired scenario generator & history condition generator
│       ├── matching/          <- State-matching metrics & verification engines
│       ├── metrics/           <- Detection, diagnosis, recovery, and discordance metrics
│       ├── rollout/           <- Trajectory collection & deterministic replay
│       └── visualization/     <- Publication and diagnostic plotting routines
├── scripts/                   <- Runnable entrypoints for benchmarks and training
├── notebooks/                 <- Pre-executed experiment and analysis notebooks
├── tests/                     <- Unit and integration test suite (pytest)
├── data/                      <- Benchmark manifests and processed evaluations
└── analysis/                  <- Contact mechanics, sensitivity, and horizon analyses
```

---

## 3. Quick Start

### Installation & Environment Setup

```bash
# Clone the repository
git clone https://github.com/sumitrajapure1308/Causal-History-Dependence-in-Robot-Policy-Recovery.git
cd Causal-History-Dependence-in-Robot-Policy-Recovery

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Verification & Test Suite

Verify environment setup and run the test suite:
```bash
# Verify environment dependencies
python scripts/check_environment.py

# Run unit and integration tests
pytest tests/
```

### Running the Confirmatory Benchmark

```bash
# Execute the paired replay-injection benchmark
python scripts/run_staged_benchmark.py

# Analyze benchmark results and evaluate McNemar / TOST statistics
python scripts/analyze_stage_c_benchmark.py
```

---

## 4. Policy Architectures Evaluated

- **Reactive MLP (Negative Control):** Memoryless feedforward controller ($k=1$ observation).
- **History GRU (Nominal Imitation):** Recurrent policy unrolling over historical observation-action trajectories.
- **Recovery-Augmented MLP:** Memoryless controller trained on targeted recovery maneuvers from physical deviations.
- **Recovery-Augmented GRU:** Recurrent controller trained on failure-to-recovery transitions.

---

## 5. Author & Licensing

- **Author:** Sumit S. Rajapure
- **Email:** sumitrajapure2006@gmail.com
- **ORCID:** [0009-0009-8899-353X](https://orcid.org/0009-0009-8899-353X)
- **Funding:** Personally funded by the author; no external funding received.

### Licensing Terms

- **Source Code & Software:** Covered under the [MIT License](LICENSE). Copyright (c) 2026 Sumit S. Rajapure.
- **Documentation, Data, & Non-Code Artifacts:** Covered under the Creative Commons Attribution 4.0 International License ([CC BY 4.0](LICENSE-DATA.md)).
