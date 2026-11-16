#!/usr/bin/env bash
set -e
echo "Running Causal-History Recovery Submission Smoke Test..."
python scripts/run_smoke_test.py
pytest tests -v
echo "Smoke test passed successfully."
