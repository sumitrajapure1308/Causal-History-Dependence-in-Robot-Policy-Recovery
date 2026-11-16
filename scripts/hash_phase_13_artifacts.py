"""Generate SHA-256 Hash Manifest for all Phase 13 Artifacts.

Saves output to results/phase_13/phase_13_file_hashes.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p13_res_dir = os.path.join(repo_root, "results", "phase_13")
os.makedirs(p13_res_dir, exist_ok=True)


def compute_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    p13_files = []

    # Docs
    docs = [
        "docs/audit/phase_12_primary_null_result_audit.md",
        "docs/audit/phase_12_continuous_null_result_audit.md",
        "docs/analysis/mechanism_result_interpretation.md",
        "docs/audit/policy_capability_limitation_audit.md",
        "docs/audit/benchmark_result_robustness_audit.md",
        "docs/manuscript/evidence_package.md",
        "docs/manuscript/paper_tables.md",
        "docs/reports/phase_13_result_interpretation_report.md",
        "PROJECT_STATUS.md",
        "docs/decision_log.md",
    ]
    for d in docs:
        p = os.path.join(repo_root, d)
        if os.path.exists(p):
            p13_files.append(d)

    # Scripts
    scripts = [
        "scripts/make_paper_figures.py",
        "scripts/build_paper_tables.py",
        "scripts/build_phase_13_notebooks.py",
        "scripts/hash_phase_13_artifacts.py",
    ]
    for s in scripts:
        p = os.path.join(repo_root, s)
        if os.path.exists(p):
            p13_files.append(s)

    # Notebooks (57 to 61)
    nb_dir = os.path.join(repo_root, "notebooks")
    if os.path.exists(nb_dir):
        for fname in os.listdir(nb_dir):
            if any(fname.startswith(f"{nb_id}_") for nb_id in range(57, 62)) and fname.endswith(".ipynb"):
                p13_files.append(os.path.join("notebooks", fname))

    # Results
    if os.path.exists(p13_res_dir):
        for root, _, files in os.walk(p13_res_dir):
            for f in files:
                if f.endswith((".json", ".jsonl")):
                    rel = os.path.relpath(os.path.join(root, f), repo_root)
                    p13_files.append(rel)

    # Paper Figures
    fig_dir = os.path.join(repo_root, "figures", "benchmark", "paper")
    if os.path.exists(fig_dir):
        for f in os.listdir(fig_dir):
            p13_files.append(os.path.join("figures", "benchmark", "paper", f))

    p13_files = sorted(list(set(p13_files)))

    manifest = {
        "metadata": {
            "project": "Causal-History Dependence in Robot Policy Recovery",
            "phase": "Phase 13 (Result Interpretation, Robustness Audit, and Manuscript Evidence Package)",
            "git_status": "unavailable (not a git repository)",
            "total_artifacts": len(p13_files),
        },
        "artifacts": {},
    }

    for rel in p13_files:
        full_path = os.path.join(repo_root, rel)
        if os.path.exists(full_path):
            manifest["artifacts"][rel.replace("\\", "/")] = {
                "sha256": compute_sha256(full_path),
                "bytes": os.path.getsize(full_path),
            }

    out_path = os.path.join(p13_res_dir, "phase_13_file_hashes.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(manifest['artifacts'])} Phase 13 artifacts -> {out_path}")


if __name__ == "__main__":
    main()

