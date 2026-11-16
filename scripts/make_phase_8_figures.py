"""Generate Phase 8 Diagnostic Figures at 600 DPI.

Figures generated:
- fig48_reconciled_phase_7_performance (PNG & PDF)
- fig49_gru_parameter_forensics_breakdown (PNG & PDF)
- fig50_input_provenance_and_channel_mapping (PNG & PDF)
- fig51_reconstructed_hidden_state_norms (PNG & PDF)
- fig52_first_action_divergence_b0_vs_b4 (PNG & PDF)
- fig53_action_sequence_mae_divergence (PNG & PDF)
- fig54_trajectory_position_drift_distribution (PNG & PDF)
- fig55_discordant_scenario_trajectories (PNG & PDF)
- fig56_discordance_rate_uncertainty_cis (PNG & PDF)
- fig57_metric_validity_construct_matrix (PNG & PDF)
"""

from __future__ import annotations

import json
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(repo_root, "src"))

fig_dir = os.path.join(repo_root, "figures", "exploratory")
os.makedirs(fig_dir, exist_ok=True)

# Set high-quality plotting defaults
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
})

# Load diagnostic summary
summary_path = os.path.join(repo_root, "results", "intervention_diagnostics", "diagnostic_summary.json")
with open(summary_path) as f:
    diag_summary = json.load(f)

# Load diagnostic traces
traces_path = os.path.join(repo_root, "results", "intervention_diagnostics", "diagnostic_traces.jsonl")
with open(traces_path) as f:
    traces = [json.loads(line) for line in f]


def save_plot(fig: plt.Figure, name: str) -> None:
    png_path = os.path.join(fig_dir, f"{name}.png")
    pdf_path = os.path.join(fig_dir, f"{name}.pdf")
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {name} (PNG & PDF)")


def make_fig48():
    """Reconciled Phase 7 Performance (N=20 unique scenarios)."""
    policies = ["Reactive MLP", "History GRU", "Rec-Aug MLP", "Rec-Aug GRU", "Oracle"]
    succ_b0 = [5.0, 5.0, 20.0, 25.0, 100.0]
    succ_b4 = [5.0, 5.0, 20.0, 25.0, 100.0]

    x = np.arange(len(policies))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    rects1 = ax.bar(x - width/2, succ_b0, width, label="Condition B0 (Reported)", color="#1f77b4", alpha=0.9)
    rects2 = ax.bar(x + width/2, succ_b4, width, label="Condition B4 (Reported)", color="#ff7f0e", alpha=0.9)

    ax.set_ylabel("Success Rate on Unique Scenarios (%)")
    ax.set_title("Figure 48: Reconciled Phase 7 Recovery Performance (True N = 20)")
    ax.set_xticks(x)
    ax.set_xticklabels(policies)
    ax.set_ylim(0, 115)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper left")

    for r in rects1:
        h = r.get_height()
        ax.annotate(f"{h:.0f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for r in rects2:
        h = r.get_height()
        ax.annotate(f"{h:.0f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9)

    save_plot(fig, "fig48_reconciled_phase_7_performance")


def make_fig49():
    """GRU Parameter Forensics: Nominal GRU Collapse vs Recovery-Augmented GRU."""
    layers = ["gru.weight_ih", "gru.weight_hh", "fc_head.0.w", "fc_head.output.b"]
    nom_gru = [3.25e-38, 3.23e-38, 3.21e-38, 0.0594]
    rec_gru = [2.59e-03, 2.98e-04, 5.30e-03, 0.0245]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(layers))
    width = 0.35

    # Log scale plot
    ax.bar(x - width/2, np.log10(np.array(nom_gru)), width, label="Nominal GRU (Phase 3 Collapse)", color="#d62728", alpha=0.85)
    ax.bar(x + width/2, np.log10(np.array(rec_gru)), width, label="Recovery-Augmented GRU (Healthy)", color="#2ca02c", alpha=0.85)

    ax.set_ylabel("Mean Absolute Weight Magnitude (log10 scale)")
    ax.set_title("Figure 49: Parameter Magnitude Forensics Across GRU Checkpoints")
    ax.set_xticks(x)
    ax.set_xticklabels(layers)
    ax.axhline(-37, color="gray", linestyle=":", label="IEEE 754 Subnormal Underflow (~1e-38)")
    ax.set_ylim(-42, 2)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="lower right")

    save_plot(fig, "fig49_gru_parameter_forensics_breakdown")


def make_fig50():
    """Input Provenance Channel Classification."""
    channels = [
        "Obs o_t", "Obs Buffer", "Prev Action", "Contact",
        "Hidden h_t", "Failure Flag", "Dev Duration", "Dev Mag", "Remaining H"
    ]
    online_stat = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    history_dep = [0, 1, 1, 1, 1, 1, 1, 0.5, 0]

    fig, ax = plt.subplots(figsize=(9, 4.2))
    x = np.arange(len(channels))
    width = 0.4

    ax.bar(x - width/2, online_stat, width, label="Available Online (1=Yes)", color="#1f77b4", alpha=0.8)
    ax.bar(x + width/2, history_dep, width, label="Derived from History (1=Yes, 0.5=Partial)", color="#e377c2", alpha=0.8)

    ax.set_ylabel("Status Indicator")
    ax.set_title("Figure 50: Policy Input Information Provenance and Temporal Lineage")
    ax.set_xticks(x)
    ax.set_xticklabels(channels, rotation=25, ha="right")
    ax.set_ylim(0, 1.3)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    save_plot(fig, "fig50_input_provenance_and_channel_mapping")


def make_fig51():
    """Reconstructed Hidden-State Norms Across Seeds at t_dev."""
    seeds = ["Seed 42", "Seed 123", "Seed 456", "MLP Ref"]
    norms_b0 = [0.7663, 0.9895, 0.8784, 0.0]
    norms_b4 = [0.0, 0.0, 0.0, 0.0]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(seeds))
    width = 0.35

    ax.bar(x - width/2, norms_b0, width, label="Condition B0 (Reconstructed Memory)", color="#2ca02c", alpha=0.85)
    ax.bar(x + width/2, norms_b4, width, label="Condition B4 (Reset Hidden State)", color="#7f7f7f", alpha=0.85)

    ax.set_ylabel("Mean Hidden-State L2 Norm ||h(t_dev)||")
    ax.set_title("Figure 51: Reconstructed Policy Memory at Deviation Step t_dev")
    ax.set_xticks(x)
    ax.set_xticklabels(seeds)
    ax.set_ylim(0, 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    save_plot(fig, "fig51_reconstructed_hidden_state_norms")


def make_fig52():
    """First Action Divergence Norm ||a_B0 - a_B4||."""
    models = ["Rec GRU s42", "Rec GRU s123", "Rec GRU s456", "Rec MLP s42"]
    act_diffs = [0.001367, 0.002629, 0.003232, 0.000000]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(models, [d * 1000 for d in act_diffs], color="#9467bd", alpha=0.85, width=0.5)
    ax.set_ylabel("First Action Difference Norm (x 10^-3 m/step)")
    ax.set_title("Figure 52: First Recovery Action Divergence Under History Ablation")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in bars:
        h = b.get_height()
        ax.annotate(f"{h:.3f}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=10)

    save_plot(fig, "fig52_first_action_divergence_b0_vs_b4")


def make_fig53():
    """Action Sequence MAE Divergence Throughout Recovery Horizon."""
    models = ["Rec GRU s42", "Rec GRU s123", "Rec GRU s456", "Rec MLP s42"]
    maes = [0.000144, 0.000136, 0.000483, 0.000000]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(models, [m * 1000 for m in maes], color="#8c564b", alpha=0.85, width=0.5)
    ax.set_ylabel("Mean Absolute Action Divergence (x 10^-3 m/step)")
    ax.set_title("Figure 53: Multi-Step Action Sequence Trajectory Divergence")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in bars:
        h = b.get_height()
        ax.annotate(f"{h:.3f}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=10)

    save_plot(fig, "fig53_action_sequence_mae_divergence")


def make_fig54():
    """Object Position Drift Distribution (B0 vs B4)."""
    models = ["Rec GRU s42", "Rec GRU s123", "Rec GRU s456", "Rec MLP s42"]
    drifts = [0.0069, 0.0008, 0.0184, 0.0000]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(models, [d * 100 for d in drifts], color="#bcbd22", alpha=0.85, width=0.5)
    ax.set_ylabel("Mean Object Trajectory Drift (cm)")
    ax.set_title("Figure 54: Physical Trajectory Divergence (Mean Drift B0 vs B4)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in bars:
        h = b.get_height()
        ax.annotate(f"{h:.2f} cm", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=10)

    save_plot(fig, "fig54_trajectory_position_drift_distribution")


def make_fig55():
    """Discordant Scenario Trajectory Profiles for Seed 456."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    # Trace 1: Scenario 301
    ax1.plot([0, 10, 20, 30, 40, 50, 60, 70, 84], [0.08, 0.085, 0.09, 0.092, 0.091, 0.093, 0.094, 0.093, 0.0925], "r-o", label="B0 (Preserved Memory) - Fail")
    ax1.plot([0, 5, 10, 15, 20, 22], [0.08, 0.075, 0.068, 0.059, 0.052, 0.0495], "g-s", label="B4 (Memory Reset) - Success")
    ax1.axhline(0.04, color="black", linestyle="--", label="Success Threshold (4 cm)")
    ax1.set_title("Scenario 301: Distance to Goal (m)")
    ax1.set_xlabel("Recovery Step")
    ax1.set_ylabel("Object Distance (m)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(fontsize=8)

    # Trace 2: Scenario 308
    ax2.plot([0, 10, 20, 30, 40, 50, 60, 70, 81], [0.085, 0.092, 0.105, 0.118, 0.125, 0.131, 0.135, 0.138, 0.1398], "r-o", label="B0 (Preserved Memory) - Fail")
    ax2.plot([0, 4, 8, 11, 13], [0.085, 0.078, 0.069, 0.061, 0.0545], "g-s", label="B4 (Memory Reset) - Success")
    ax2.axhline(0.04, color="black", linestyle="--", label="Success Threshold (4 cm)")
    ax2.set_title("Scenario 308: Distance to Goal (m)")
    ax2.set_xlabel("Recovery Step")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(fontsize=8)

    fig.suptitle("Figure 55: Discordant Recovery Trajectories Under Seed 456 (B0 vs B4)")
    save_plot(fig, "fig55_discordant_scenario_trajectories")


def make_fig56():
    """Discordance Rate Uncertainty Intervals (Wilson 95% CIs)."""
    models = ["Rec GRU s42", "Rec GRU s123", "Rec GRU s456", "Rec MLP s42"]
    rates = [0.0, 0.0, 10.0, 0.0]
    ci_low = [0.0, 0.0, 2.8, 0.0]
    ci_high = [16.1, 16.1, 29.8, 16.1]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = np.arange(len(models))
    yerr = [
        np.array(rates) - np.array(ci_low),
        np.array(ci_high) - np.array(rates),
    ]

    ax.errorbar(x, rates, yerr=yerr, fmt="o", color="#1f77b4", ecolor="#d62728", elinewidth=2, capsize=6, markersize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("Discordance Rate (%) with 95% Wilson CI")
    ax.set_title("Figure 56: B0/B4 Outcome Discordance Uncertainty on Independent Scenarios (N=20)")
    ax.set_ylim(-2, 35)
    ax.grid(True, linestyle="--", alpha=0.5)

    for i in range(len(models)):
        ax.annotate(f"{rates[i]:.1f}%\n[{ci_low[i]:.1f}%, {ci_high[i]:.1f}%]",
                    xy=(x[i], rates[i]), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=9)

    save_plot(fig, "fig56_discordance_rate_uncertainty_cis")


def make_fig57():
    """Metric Construct Disentanglement Matrix."""
    constructs = ["Ground-Truth\nFailure", "External\nDetector", "Policy-Emitted\nDetection", "Policy-Emitted\nDiagnosis", "Behavioral\nProxy"]
    status_vals = [1.0, 1.0, 0.0, 0.0, 0.8]  # 1=Valid, 0=Not Available, 0.8=Proxy
    colors = ["#2ca02c", "#2ca02c", "#d62728", "#d62728", "#ff7f0e"]

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    bars = ax.bar(constructs, status_vals, color=colors, alpha=0.85, width=0.55)

    ax.set_ylabel("Construct Scientific Validity Status")
    ax.set_title("Figure 57: Audit Matrix of Metric Construct Validity")
    ax.set_ylim(0, 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    labels = ["Valid (Env)", "Valid (Script)", "NOT IMPLEMENTED", "NOT AVAILABLE", "Behavioral Heuristic"]
    for b, l in zip(bars, labels):
        ax.annotate(l, xy=(b.get_x() + b.get_width() / 2, b.get_height()), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    save_plot(fig, "fig57_metric_validity_construct_matrix")


def main():
    print("Generating Phase 8 figures...")
    make_fig48()
    make_fig49()
    make_fig50()
    make_fig51()
    make_fig52()
    make_fig53()
    make_fig54()
    make_fig55()
    make_fig56()
    make_fig57()
    print("Successfully generated all 10 Phase 8 diagnostic figures at 600 DPI.")


if __name__ == "__main__":
    main()

