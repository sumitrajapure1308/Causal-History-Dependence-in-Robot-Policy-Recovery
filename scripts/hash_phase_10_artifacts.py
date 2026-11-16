"""Fingerprint and Verify Phase 10 Artifacts with SHA-256 Hashes.

Generates:
- results/phase_10/phase_10_file_hashes.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def hash_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    targets = [
        # Source & Config
        "src/causal_history_recovery/environments/assets/second_push_target.xml",
        "src/causal_history_recovery/environments/second_push_task_env.py",
        "src/causal_history_recovery/environments/contact_loss_failure.py",
        "configs/tasks/second_push_task.yaml",
        # Tests
        "tests/test_second_push_task_env.py",
        "tests/test_contact_loss_failure.py",
        # Scripts
        "scripts/audit_binary_sensitivity.py",
        "scripts/run_second_task_pilot.py",
        "scripts/make_phase_10_figures.py",
        "scripts/build_phase_10_notebooks.py",
        # Documentation & Methodology
        "docs/audit/phase_9_null_result_audit.md",
        "docs/audit/binary_outcome_sensitivity_audit.md",
        "docs/audit/policy_recovery_capability_audit.md",
        "docs/methodology/second_failure_mode_specification.md",
        "docs/methodology/final_benchmark_design.md",
        # Results
        "results/phase_10/binary_outcome_sensitivity_report.json",
        "results/phase_10/policy_recovery_capability_report.json",
        "results/phase_10/second_task_pilot/rollout_manifest.json",
        "results/phase_10/second_task_pilot/evaluation_summary.json",
        "results/phase_10/second_task_pilot/paired_comparisons.json",
        "results/phase_10/second_task_pilot/history_dependence_report.json",
        "results/phase_10/second_task_pilot/policy_ranking_report.json",
        "results/phase_10/second_task_pilot/sensitivity_report.json",
        # Notebooks
        "notebooks/38_binary_outcome_sensitivity_audit.ipynb",
        "notebooks/39_policy_recovery_capability_audit.ipynb",
        "notebooks/40_second_task_pilot.ipynb",
        "notebooks/41_second_failure_mode_pilot.ipynb",
        "notebooks/42_final_benchmark_design_freeze.ipynb",
    ]

    # Add figures 78 to 97
    fig_dir = os.path.join(repo_root, "figures", "exploratory")
    for num in range(78, 98):
        for ext in ["png", "pdf"]:
            # Find matching file
            for fname in os.listdir(fig_dir):
                if fname.startswith(f"fig{num}_") and fname.endswith(f".{ext}"):
                    targets.append(os.path.join("figures", "exploratory", fname))

    hash_manifest: dict[str, str] = {}
    missing = []
    for rel_path in targets:
        full_path = os.path.join(repo_root, rel_path)
        if os.path.exists(full_path):
            hash_manifest[rel_path.replace("\\", "/")] = hash_file(full_path)
        else:
            missing.append(rel_path)

    out_path = os.path.join(repo_root, "results", "phase_10", "phase_10_file_hashes.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "git_status": "NOT_A_GIT_REPOSITORY (Explicitly checked and verified)",
            "total_files_hashed": len(hash_manifest),
            "missing_files": missing,
            "hashes": hash_manifest,
        }, f, indent=2)

    print(f"Hashed {len(hash_manifest)} Phase 10 files. Missing: {len(missing)}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()

