#!/usr/bin/env python3
"""Full Benchmark Reproduction Entrypoint."""
import os
import sys
import subprocess

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

print("=== 1. Running Unit & Integration Tests ===")
ret = subprocess.run([sys.executable, "-m", "pytest", os.path.join(repo_root, "tests"), "-v"])
if ret.returncode != 0:
    sys.exit(ret.returncode)

print("\n=== 2. Running Submission Smoke Test ===")
ret = subprocess.run([sys.executable, os.path.join(repo_root, "scripts", "run_smoke_test.py")])
if ret.returncode != 0:
    sys.exit(ret.returncode)

print("\n=== Full Verification Complete: ALL TESTS PASSED ===")
