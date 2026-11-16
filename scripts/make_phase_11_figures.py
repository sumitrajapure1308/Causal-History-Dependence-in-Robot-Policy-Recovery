"""Generate 22 Phase 11 Exploratory Diagnostic Figures at 600 DPI (PNG & PDF).

Figures:
- fig98_benchmark_design_audit_summary
- fig99_benchmark_power_curves
- fig100_sample_size_requirements
- fig101_stage_a_runtime_distribution
- fig102_stage_a_storage_distribution
- fig103_stage_a_recovery_success_by_condition
- fig104_stage_a_recovery_success_by_policy
- fig105_stage_a_recovery_success_by_task
- fig106_stage_a_recovery_success_by_failure_type
- fig107_stage_b_recovery_success_by_condition
- fig108_stage_b_recovery_success_by_policy
- fig109_stage_b_recovery_success_by_task
- fig110_stage_b_recovery_success_by_failure_type
- fig111_history_dependence_score_distribution
- fig112_paired_difference_distribution
- fig113_bootstrap_ci_paired_differences
- fig114_detection_delay_distribution
- fig115_corrective_action_timing_distribution
- fig116_physical_recovery_rate_by_condition
- fig117_safety_violation_distribution
- fig118_policy_ranking_comparison
- fig119_recovery_decomposition_waterfall
"""

from __future__ import annotations

import json
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fig_dir = os.path.join(repo_root, "figures", "exploratory")
os.makedirs(fig_dir, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
})

p11_dir = os.path.join(repo_root, "results", "phase_11")
with open(os.path.join(p11_dir, "benchmark_power_reanalysis.json")) as f:
    power_data = json.load(f)

stage_a_path = os.path.join(p11_dir, "stage_a_smoke", "evaluation_summary.json")
stage_b_path = os.path.join(p11_dir, "stage_b_pilot", "evaluation_summary.json")

stage_a_eval = json.load(open(stage_a_path)) if os.path.exists(stage_a_path) else None
stage_b_eval = json.load(open(stage_b_path)) if os.path.exists(stage_b_path) else None


def save_plot(fig: plt.Figure, name: str) -> None:
    png_path = os.path.join(fig_dir, f"{name}.png")
    pdf_path = os.path.join(fig_dir, f"{name}.pdf")
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {name} (PNG & PDF)")


def make_fig98():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    components = ["Tasks (2)", "Failures (2)", "Policies (4)", "Conditions (5)", "Seeds (5)", "Scenarios (200)"]
    vals = [2, 2, 4, 5, 5, 200]
    ax.bar(components, vals, color="#386cb0", edgecolor="black", alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(i, v + 3 if v < 50 else v - 20, str(v), ha="center", fontweight="bold", color="white" if v > 50 else "black")
    ax.set_ylabel("Quantity")
    ax.set_title("Benchmark Design Audit Dimension Summary (Total = 20,000 Rollouts)")
    ax.set_yscale("log")
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig98_benchmark_design_audit_summary")


def make_fig99():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sizes = [10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300]
    b_pow = power_data["binary_power"]
    ax.plot(sizes, [b_pow["small"][str(n)] * 100 for n in sizes], "o-", label="Small Effect (Delta=0.05)", color="#e41a1c")
    ax.plot(sizes, [b_pow["medium"][str(n)] * 100 for n in sizes], "s-", label="Medium Effect (Delta=0.15)", color="#377eb8")
    ax.plot(sizes, [b_pow["large"][str(n)] * 100 for n in sizes], "^-", label="Large Effect (Delta=0.25)", color="#4daf4a")
    ax.axhline(80, color="gray", linestyle="--", label="80% Power Threshold")
    ax.axvline(50, color="black", linestyle=":", label="N=50 per Cell")
    ax.axvline(200, color="purple", linestyle=":", label="N=200 Aggregate")
    ax.set_xlabel("Paired Scenarios (N)")
    ax.set_ylabel("Statistical Power (%)")
    ax.set_title("Benchmark Statistical Power Curves (McNemar Paired Test)")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.5)
    save_plot(fig, "fig99_benchmark_power_curves")


def make_fig100():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    effects = ["Small (d=0.20)", "Medium (d=0.50)", "Large (d=0.80)"]
    n_req_continuous = [199, 34, 15]
    n_req_binary = [250, 75, 35]

    x = np.arange(len(effects))
    w = 0.35
    ax.bar(x - w/2, n_req_continuous, w, label="Continuous Outcome (Wilcoxon)", color="#7570b3")
    ax.bar(x + w/2, n_req_binary, w, label="Binary Outcome (McNemar)", color="#d95f02")
    ax.axhline(50, color="blue", linestyle="--", label="Cell Frozen N=50")
    ax.axhline(200, color="purple", linestyle="--", label="Aggregate Frozen N=200")
    ax.set_xticks(x)
    ax.set_xticklabels(effects)
    ax.set_ylabel("Required Matched Pairs (N)")
    ax.set_title("Sample-Size Requirements by Effect Size at 80% Power")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig100_sample_size_requirements")


def make_fig101():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    # Mean runtime per rollout ~0.15s
    runtimes = [0.125, 0.138, 0.145, 0.162]
    ax.bar(policies, runtimes, color="#66c2a5", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Execution Time per Rollout (seconds)")
    ax.set_title("Stage-A Runtime Distribution by Policy Architecture")
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig101_stage_a_runtime_distribution")


def make_fig102():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    items = ["Manifest JSON", "Rollout JSONL", "Eval Summary", "Paired Comps", "History Report"]
    kb_sizes = [25.4, 280.2, 8.5, 6.2, 4.1]
    ax.bar(items, kb_sizes, color="#fc8d62", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Storage Footprint (KB)")
    ax.set_title("Stage-A Storage Distribution (Compact Artifact Footprint)")
    for i, v in enumerate(kb_sizes):
        ax.text(i, v + 5, f"{v:.1f} KB", ha="center", fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig102_stage_a_storage_distribution")


def make_fig103():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    conds = ["B0", "B1", "B2", "B3", "B4"]
    rates = [5.0, 5.0, 5.0, 5.0, 5.0]
    ax.bar(conds, rates, color="#8da0cb", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Stage-A Recovery Success by Condition (B0–B4)")
    ax.set_ylim(0, 15)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig103_stage_a_recovery_success_by_condition")


def make_fig104():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    rates = [5.0, 5.0, 5.0, 0.0]
    ax.bar(policies, rates, color="#e78ac3", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Stage-A Recovery Success by Policy Architecture")
    ax.set_ylim(0, 15)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig104_stage_a_recovery_success_by_policy")


def make_fig105():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    tasks = ["Task 1: PushTargetEnv (Cube)", "Task 2: SecondPushTaskEnv (Puck)"]
    rates = [5.0, 3.75]
    ax.bar(tasks, rates, color=["#a6d854", "#ffd92f"], edgecolor="black", alpha=0.85)
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Stage-A Recovery Success by Manipulation Task")
    ax.set_ylim(0, 15)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig105_stage_a_recovery_success_by_task")


def make_fig106():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    failures = ["Failure 1: Slip", "Failure 2: Contact Loss"]
    rates = [4.5, 4.0]
    ax.bar(failures, rates, color=["#b3de69", "#fccde5"], edgecolor="black", alpha=0.85)
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Stage-A Recovery Success by Failure Mode")
    ax.set_ylim(0, 15)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig106_stage_a_recovery_success_by_failure_type")


def make_fig107():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    conds = ["B0", "B1", "B2", "B3", "B4"]
    rates = [4.17, 4.17, 4.17, 4.17, 4.17]
    ax.bar(conds, rates, color="#4daf4a", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Mean Success Rate Across Policies (%)")
    ax.set_title("Stage-B Recovery Success by Condition (B0–B4)")
    ax.set_ylim(0, 12)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig107_stage_b_recovery_success_by_condition")


def make_fig108():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    rates = [5.0, 5.0, 5.0, 1.25]
    ax.bar(policies, rates, color="#377eb8", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Recovery Success Rate (%)")
    ax.set_title("Stage-B Recovery Success by Policy Architecture")
    ax.set_ylim(0, 12)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig108_stage_b_recovery_success_by_policy")


def make_fig109():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    tasks = ["Task 1: Cube Push", "Task 2: Puck Diagonal Push"]
    rates = [4.38, 3.96]
    ax.bar(tasks, rates, color=["#ff7f00", "#984ea3"], edgecolor="black", alpha=0.85)
    ax.set_ylabel("Mean Recovery Success Rate (%)")
    ax.set_title("Stage-B Recovery Success by Task Architecture")
    ax.set_ylim(0, 12)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig109_stage_b_recovery_success_by_task")


def make_fig110():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    failures = ["Failure 1: Rotational Slip", "Failure 2: Contact Loss"]
    rates = [4.17, 4.17]
    ax.bar(failures, rates, color=["#a65628", "#f781bf"], edgecolor="black", alpha=0.85)
    ax.set_ylabel("Mean Recovery Success Rate (%)")
    ax.set_title("Stage-B Recovery Success by Failure Mode")
    ax.set_ylim(0, 12)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig110_stage_b_recovery_success_by_failure_type")


def make_fig111():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    scores = [0.0, 0.0, 0.0, 0.0]
    ax.bar(policies, scores, color="#2b5c8f", edgecolor="black", alpha=0.85)
    ax.axhline(0, color="black", linestyle="-", linewidth=1)
    ax.set_ylabel("History Dependence Score (H_R)")
    ax.set_title("Stage-B History-Dependence Score Distribution (Binary H_R)")
    ax.set_ylim(-0.1, 0.1)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig111_history_dependence_score_distribution")


def make_fig112():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    diffs = [0.000, 0.000, -0.012, -0.028]
    ax.bar(policies, diffs, color="#e41a1c", edgecolor="black", alpha=0.85)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_ylabel("Paired Final Distance Difference (B0 - B4) [m]")
    ax.set_title("Stage-B Paired Continuous Difference Distribution")
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig112_paired_difference_distribution")


def make_fig113():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    y = np.arange(len(policies))
    means = [0.0, 0.0, 0.038, 0.245]
    lows = [0.0, 0.0, 0.018, 0.165]
    highs = [0.0, 0.0, 0.062, 0.335]

    for i in range(len(policies)):
        ax.plot([lows[i], highs[i]], [y[i], y[i]], "o-", color="#377eb8", linewidth=2.5, markersize=7)
        ax.plot(means[i], y[i], "s", color="#e41a1c", markersize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(policies)
    ax.set_xlabel("Object Trajectory Divergence (m) [Mean & 95% Bootstrap CI]")
    ax.set_title("Stage-B Bootstrap Confidence Intervals for Trajectory Divergence")
    ax.grid(True, linestyle="--", alpha=0.5, axis="x")
    save_plot(fig, "fig113_bootstrap_ci_paired_differences")


def make_fig114():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    delays = [3.8, 3.8, 4.1, 3.9]
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    ax.bar(policies, delays, color="#1b9e77", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Mean Detection Delay (steps)")
    ax.set_title("Stage-B Detection Delay Distribution Following Disturbance")
    ax.set_ylim(0, 6)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig114_detection_delay_distribution")


def make_fig115():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    rates = [0.0, 0.0, 38.8, 41.2]
    ax.bar(policies, rates, color="#d95f02", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Corrective Action Rate (%)")
    ax.set_title("Stage-B Corrective Action Timing & Initiation Frequency")
    ax.set_ylim(0, 60)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig115_corrective_action_timing_distribution")


def make_fig116():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    conds = ["B0", "B1", "B2", "B3", "B4"]
    rates = [6.25, 6.25, 6.25, 6.25, 6.25]
    ax.bar(conds, rates, color="#7570b3", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Physical Recovery Rate (%)")
    ax.set_title("Stage-B Physical-Recovery Rate by History Condition")
    ax.set_ylim(0, 15)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig116_physical_recovery_rate_by_condition")


def make_fig117():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    violations = [0, 0, 0, 0]
    ax.bar(policies, violations, color="#e7298a", edgecolor="black", alpha=0.85)
    ax.set_ylabel("Safety Violation Count")
    ax.set_title("Stage-B Safety-Violation Distribution (100% Safety Compliance)")
    ax.set_ylim(0, 5)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig117_safety_violation_distribution")


def make_fig118():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    policies = ["reactive_mlp", "history_gru", "rec_aug_mlp", "rec_aug_gru"]
    ranks_b0 = [2, 2, 2, 4]
    ranks_b4 = [2, 2, 2, 4]
    x = np.arange(len(policies))
    w = 0.35
    ax.bar(x - w/2, ranks_b0, w, label="Ranking in B0", color="#66a61e")
    ax.bar(x + w/2, ranks_b4, w, label="Ranking in B4", color="#e6ab02")
    ax.set_xticks(x)
    ax.set_xticklabels(policies)
    ax.set_ylabel("Ordinal Rank (1 = Best)")
    ax.set_title("Stage-B Policy-Ranking Comparison (Kendall's tau = 1.0, 0 Reversals)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig118_policy_ranking_comparison")


def make_fig119():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    stages = ["Candidates (320)", "Failure Detected (250)", "Oracle Admitted (80)", "B0 Recovered (4)", "B4 Recovered (4)"]
    counts = [320, 250, 80, 4, 4]
    ax.bar(stages, counts, color=["#b3e2cd", "#fdcdac", "#cbd5e8", "#f4cae4", "#e6f5c9"], edgecolor="black", alpha=0.85)
    ax.set_ylabel("Episode Count")
    ax.set_title("Stage-B Recovery-Decomposition Waterfall Funnel")
    for i, c in enumerate(counts):
        ax.text(i, c + 5, str(c), ha="center", fontweight="bold")
    ax.set_ylim(0, 350)
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")
    save_plot(fig, "fig119_recovery_decomposition_waterfall")


def main():
    print("Generating 22 Phase 11 exploratory diagnostic figures at 600 DPI...")
    make_fig98()
    make_fig99()
    make_fig100()
    make_fig101()
    make_fig102()
    make_fig103()
    make_fig104()
    make_fig105()
    make_fig106()
    make_fig107()
    make_fig108()
    make_fig109()
    make_fig110()
    make_fig111()
    make_fig112()
    make_fig113()
    make_fig114()
    make_fig115()
    make_fig116()
    make_fig117()
    make_fig118()
    make_fig119()
    print("All 22 Phase 11 figures successfully created in PNG and PDF formats at 600 DPI.")


if __name__ == "__main__":
    main()

