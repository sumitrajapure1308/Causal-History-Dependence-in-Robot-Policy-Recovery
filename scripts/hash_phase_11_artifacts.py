"""Generate SHA-256 Hash Manifest for all Phase 11 Artifacts.

Saves output to results/phase_11/phase_11_file_hashes.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def compute_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    p11_files = []

    # Docs
    docs = [
        "docs/audit/final_benchmark_design_audit.md",
        "docs/methodology/benchmark_outcome_hierarchy.md",
        "docs/methodology/staged_benchmark_execution_plan.md",
        "docs/statistics/final_benchmark_power_reanalysis.md",
        "docs/reports/phase_11_benchmark_readiness_report.md",
    ]
    for d in docs:
        p = os.path.join(repo_root, d)
        if os.path.exists(p):
            p11_files.append(d)

    # Scripts
    scripts = [
        "scripts/reestimate_benchmark_power.py",
        "scripts/run_staged_benchmark.py",
        "scripts/make_phase_11_figures.py",
        "scripts/build_phase_11_notebooks.py",
        "scripts/hash_phase_11_artifacts.py",
    ]
    for s in scripts:
        p = os.path.join(repo_root, s)
        if os.path.exists(p):
            p11_files.append(s)

    # Notebooks
    for nb_id in range(43, 48):
        for fname in os.listdir(os.path.join(repo_root, "notebooks")):
            if fname.startswith(f"{nb_id}_") and fname.endswith(".ipynb"):
                p11_files.append(os.path.join("notebooks", fname))

    # Results
    p11_res_dir = os.path.join(repo_root, "results", "phase_11")
    for root, _, files in os.walk(p11_res_dir):
        for f in files:
            if f.endswith((".json", ".jsonl")):
                rel = os.path.relpath(os.path.join(root, f), repo_root)
                p11_files.append(rel)

    # Figures
    fig_dir = os.path.join(repo_root, "figures", "exploratory")
    for f in os.listdir(fig_dir):
        if any(f.startswith(f"fig{i}_") for i in range(98, 120)):
            p11_files.append(os.path.join("figures", "exploratory", f))

    p11_files = sorted(list(set(p11_files)))

    manifest = {
        "metadata": {
            "project": "Causal-History Dependence in Robot Policy Recovery",
            "phase": "Phase 11 (Benchmark-Readiness Audit and Staged Pilot-Scale Confirmation)",
            "total_artifacts": len(p11_files),
        },
        "artifacts": {},
    }

    for rel in p11_files:
        full_path = os.path.join(repo_root, rel)
        if os.path.exists(full_path):
            manifest["artifacts"][rel.replace("\\", "/")] = {
                "sha256": compute_sha256(full_path),
                "bytes": os.path.getsize(full_path),
            }

    out_path = os.path.join(p11_res_dir, "phase_11_file_hashes.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(manifest['artifacts'])} Phase 11 artifacts -> {out_path}")


if __name__ == "__main__":
    main()

