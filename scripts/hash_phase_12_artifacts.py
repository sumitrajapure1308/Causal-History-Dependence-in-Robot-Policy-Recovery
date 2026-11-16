"""Generate SHA-256 Hash Manifest for all Phase 12 Benchmark Artifacts.

Saves output to results/phase_12_stage_c/phase_12_file_hashes.json.
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
    p12_files = []

    # Docs
    docs = [
        "docs/methodology/phase_12_stage_c_preregistration.md",
        "docs/reports/phase_12_execution_completion_report.md",
        "docs/reports/phase_12_stage_c_benchmark_report.md",
        "docs/audit/phase_12_execution_completeness_audit.md",
        "docs/audit/phase_12_scenario_integrity_audit.md",
        "docs/audit/phase_12_condition_integrity_audit.md",
        "docs/audit/phase_12_data_integrity_audit.md",
        "docs/audit/phase_12_reproducibility_audit.md",
        "docs/audit/phase_12_analysis_readiness_audit.md",
        "docs/analysis/primary_outcome_analysis.md",
        "docs/analysis/continuous_outcome_analysis.md",
        "docs/analysis/mechanism_diagnostics_analysis.md",
        "docs/analysis/policy_ranking_analysis.md",
        "docs/analysis/sensitivity_audit_analysis.md",
    ]
    for d in docs:
        p = os.path.join(repo_root, d)
        if os.path.exists(p):
            p12_files.append(d)

    # Scripts
    scripts = [
        "scripts/run_stage_c_benchmark.py",
        "scripts/verify_stage_c_integrity.py",
        "scripts/verify_analysis_readiness.py",
        "scripts/analyze_stage_c_benchmark.py",
        "scripts/make_phase_12_figures.py",
        "scripts/build_phase_12_notebooks.py",
        "scripts/hash_phase_12_artifacts.py",
    ]
    for s in scripts:
        p = os.path.join(repo_root, s)
        if os.path.exists(p):
            p12_files.append(s)

    # Configuration files
    configs = [
        "pyproject.toml",
        "PROJECT_STATUS.md",
        "docs/decision_log.md",
    ]
    for c in configs:
        p = os.path.join(repo_root, c)
        if os.path.exists(p):
            p12_files.append(c)

    # Policy Checkpoints
    ckpts = [
        "models/checkpoints/reactive_mlp_best.pt",
        "models/checkpoints/history_gru_best.pt",
        "models/checkpoints/recovery_augmented_mlp_best.pt",
        "models/checkpoints/recovery_augmented_gru_best.pt",
    ]
    for c in ckpts:
        p = os.path.join(repo_root, c)
        if os.path.exists(p):
            p12_files.append(c)

    # Notebooks (48 to 56)
    nb_dir = os.path.join(repo_root, "notebooks")
    if os.path.exists(nb_dir):
        for fname in os.listdir(nb_dir):
            if any(fname.startswith(f"{nb_id}_") for nb_id in range(48, 57)) and fname.endswith(".ipynb"):
                p12_files.append(os.path.join("notebooks", fname))

    # Results
    p12_res_dir = os.path.join(repo_root, "results", "phase_12_stage_c")
    if os.path.exists(p12_res_dir):
        for root, _, files in os.walk(p12_res_dir):
            for f in files:
                if f.endswith((".json", ".jsonl")):
                    rel = os.path.relpath(os.path.join(root, f), repo_root)
                    p12_files.append(rel)

    # Figures
    fig_dir = os.path.join(repo_root, "figures", "benchmark")
    if os.path.exists(fig_dir):
        for f in os.listdir(fig_dir):
            if f.startswith("fig_bench_"):
                p12_files.append(os.path.join("figures", "benchmark", f))

    p12_files = sorted(list(set(p12_files)))

    manifest = {
        "metadata": {
            "project": "Causal-History Dependence in Robot Policy Recovery",
            "phase": "Phase 12 (Official Confirmatory Stage C Benchmark Execution)",
            "git_status": "unavailable (not a git repository)",
            "total_artifacts": len(p12_files),
        },
        "artifacts": {},
    }

    for rel in p12_files:
        full_path = os.path.join(repo_root, rel)
        if os.path.exists(full_path):
            manifest["artifacts"][rel.replace("\\", "/")] = {
                "sha256": compute_sha256(full_path),
                "bytes": os.path.getsize(full_path),
            }

    out_path = os.path.join(p12_res_dir, "phase_12_file_hashes.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Hashed {len(manifest['artifacts'])} Phase 12 artifacts -> {out_path}")


if __name__ == "__main__":
    main()

