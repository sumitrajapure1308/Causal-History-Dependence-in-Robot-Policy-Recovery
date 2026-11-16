# Installation Guide: Causal-History Policy Recovery Benchmark

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
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
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
