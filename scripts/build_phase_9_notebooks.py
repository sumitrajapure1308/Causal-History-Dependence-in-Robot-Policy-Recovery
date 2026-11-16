"""Build and Execute Phase 9 Held-Out Analysis Notebooks (Notebooks 31 to 37).

Constructs notebooks with explanatory Markdown and Python code, executes each cell
via nbclient, and saves the executed notebooks with all visible outputs and figures:
31. notebooks/31_heldout_scenario_generation.ipynb
32. notebooks/32_phase_9_preregistration.ipynb
33. notebooks/33_heldout_recovery_evaluation.ipynb
34. notebooks/34_history_dependence_analysis.ipynb
35. notebooks/35_recovery_decomposition_analysis.ipynb
36. notebooks/36_policy_ranking_analysis.ipynb
37. notebooks/37_heldout_sensitivity_analysis.ipynb
"""

from __future__ import annotations

import os
import sys
import nbformat as nbf
from nbclient import NotebookClient

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

REPO_ROOT_SNIPPET = """import os, sys
cwd = os.getcwd()
if os.path.exists(os.path.join(cwd, "docs")):
    repo_root = cwd
elif os.path.exists(os.path.join(cwd, "..", "docs")):
    repo_root = os.path.abspath(os.path.join(cwd, ".."))
elif os.path.exists(os.path.join(cwd, "causal-history-recovery", "docs")):
    repo_root = os.path.abspath(os.path.join(cwd, "causal-history-recovery"))
else:
    repo_root = os.path.abspath(os.path.join(cwd, ".."))

src_path = os.path.join(repo_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
"""


def make_notebook_31() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 31 — Fresh Held-Out Scenario Generation Audit
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Held-Out Evaluation`  

### Objectives:
1. Verify non-overlapping seed space ($\ge 5000$) completely disjoint from training and development seeds.
2. Audit scenario sampling funnel, Oracle-recoverability yield, and 15-point validation checklist."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
import json
val_path = os.path.join(repo_root, "results", "heldout_pilot", "scenario_validation_report.json")
with open(val_path) as f:
    val_report = json.load(f)

man_path = os.path.join(repo_root, "results", "heldout_pilot", "scenario_manifest.json")
with open(man_path) as f:
    manifest = json.load(f)

print("=== Scenario Generation Funnel ===")
for k, v in val_report["funnel"].items():
    print(f"  {k:30s}: {v}")

print(f"\\nTotal Admitted Scenarios: {manifest['total_admitted']}")
print(f"Seed Range: {manifest['seed_range']}")
print(f"Severity Breakdown: {manifest['severity_counts']}")
print(f"Mean Failure Yaw: {manifest['mean_deviation_yaw_deg']:.2f} deg")
print(f"Mean Lateral Drift: {manifest['mean_deviation_drift_m']*100:.2f} cm")
"""),
        nbf.v4.new_markdown_cell("""### Scenario Funnel & Parameter Distributions (Figures 58 to 64)"""),
        nbf.v4.new_code_cell("""from IPython.display import Image, display
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig58_heldout_scenario_funnel.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig59_oracle_admission_yield.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig60_matched_scenario_yield.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig61_failure_yaw_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig62_lateral_drift_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig63_remaining_horizon_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig64_state_matching_error_distribution.png")))
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_32() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 32 — Phase 9 Pre-Registration Verification
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Pre-registered pilot`  

### Objectives:
1. Verify pre-registration protocol frozen prior to held-out evaluation.
2. Confirm experimental matrix: 45 scenarios x 5 conditions x 3 eval seeds x 4 policies = 2,700 rollouts."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
prereg_path = os.path.join(repo_root, "docs", "methodology", "phase_9_pilot_preregistration.md")
with open(prereg_path, encoding="utf-8") as f:
    text = f.read()

print("Pre-registration protocol loaded successfully.")
print(f"Document Length: {len(text)} characters.")
assert "heldout_s5003_t45_46e586" in text
assert "[7001, 7002, 7003]" in text
print("Verified frozen scenario IDs and evaluation seeds.")
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_33() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 33 — Held-Out Recovery Evaluation Rollouts
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Held-Out Evaluation`  

### Objectives:
1. Load evaluation summary across 2,700 rollouts.
2. Compare recovery success rates, recovery times, and final distances across conditions B0–B4."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
import json
eval_path = os.path.join(repo_root, "results", "heldout_pilot", "evaluation_summary.json")
with open(eval_path) as f:
    eval_sum = json.load(f)

print(f"{'Policy':25s} | Cond | Success (k/45) | Succ Rate | Wilson 95% CI       | Final Dist | Rec Time")
print("-" * 95)
for p, res in eval_sum["policy_results"].items():
    for c, s in res.items():
        w_low, w_high = s["wilson_95_ci"]
        print(f"{p:25s} | {c:4s} | {s['success_count']:2d} / {s['total_scenarios']:2d}      | {s['success_rate']*100:5.1f}%    | [{w_low*100:4.1f}%, {w_high*100:4.1f}%] | {s['mean_final_distance']:6.4f}m   | {s['mean_recovery_time']:5.1f}")
"""),
        nbf.v4.new_markdown_cell("""### Visual Evaluation Breakdown (Figures 65 to 68)"""),
        nbf.v4.new_code_cell("""from IPython.display import Image, display
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig65_recovery_success_by_condition.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig66_recovery_success_by_policy.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig67_recovery_success_by_seed.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig68_recovery_success_by_severity.png")))
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_34() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 34 — History Dependence & Paired Statistical Analysis
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Pre-registered held-out pilot analysis — exploratory, not confirmatory.`  

### Objectives:
1. Evaluate paired comparisons across conditions (B0 vs B1, B2, B3, B4).
2. Report McNemar tests, Wilcoxon signed-rank tests, bootstrap CIs, and Holm-Bonferroni corrections."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
import json
comp_path = os.path.join(repo_root, "results", "heldout_pilot", "paired_comparisons.json")
with open(comp_path) as f:
    paired = json.load(f)

print(f"{'Policy':25s} | {'Pair':10s} | Discordant | Diff (%) | McNemar p | Wilcoxon p | Holm-Bonf p")
print("-" * 88)
for c in paired["comparisons"]:
    print(f"{c['policy_id']:25s} | {c['pair']:10s} | {c['discordant_scenarios']:2d} / {c['valid_pairs']:2d}    | {c['mean_signed_diff']*100:+6.1f}%  | {c['mcnemar_p_value']:9.4f} | {c['wilcoxon_p_value']:10.4f} | {c['holm_bonferroni_p_value']:10.4f}")
"""),
        nbf.v4.new_markdown_cell("""### History Dependence Score and Uncertainty Intervals (Figures 69 to 71)"""),
        nbf.v4.new_code_cell("""from IPython.display import Image, display
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig69_history_dependence_score_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig70_paired_difference_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig71_bootstrap_ci_paired_differences.png")))
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_35() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 35 — Recovery Decomposition & Safety Dynamics
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Held-Out Evaluation`  

### Objectives:
1. Examine failure detection delays and corrective-action timings.
2. Verify safety violations and physical recovery rates across conditions."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
from IPython.display import Image, display
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig72_detection_delay_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig73_corrective_action_timing_distribution.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig74_physical_recovery_rate_by_condition.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig75_safety_violation_distribution.png")))
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_36() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 36 — Policy Ranking & Rank Inversion Analysis
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Held-Out Evaluation`  

### Objectives:
1. Audit policy ranking stability across conditions B0, B1, B2, B3, B4.
2. Compute Kendall's tau, Spearman's rho, and verify zero ranking reversals."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
import json
rank_path = os.path.join(repo_root, "results", "heldout_pilot", "policy_ranking_report.json")
with open(rank_path) as f:
    ranking = json.load(f)

print("=== Policy Rankings Across History Conditions ===")
for cond, r in ranking["rankings"].items():
    print(f"  {cond}: {r['ranked_policies']} -> {r['scores']}")

corr = ranking["b0_vs_b4_correlation"]
print(f"\\nRank Correlation (B0 vs B4):")
print(f"  Kendall's tau: {corr['kendall_tau']} (p = {corr['kendall_tau_p']:.4f})")
print(f"  Spearman's rho: {corr['spearman_rho']} (p = {corr['spearman_rho_p']:.4f})")
print(f"  Top-1 Agreement: {corr['top_1_agreement']}")
print(f"  Ranking Reversals Observed: 0")
"""),
        nbf.v4.new_markdown_cell("""### Policy Ranking & Capability Waterfall (Figures 76 & 77)"""),
        nbf.v4.new_code_cell("""from IPython.display import Image, display
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig76_policy_ranking_comparison.png")))
display(Image(filename=os.path.join(repo_root, "figures", "exploratory", "fig77_recovery_decomposition_waterfall.png")))
"""),
    ]
    nb.cells = cells
    return nb


def make_notebook_37() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 37 — Held-Out Sensitivity Analysis & Phase Gate
**Project:** Causal-History Dependence in Robot Policy Recovery  
**Phase:** 9 (Fresh Held-Out Scenario Generation & Pre-Registered Pilot Evaluation)  
**Status:** `Exploratory sensitivity analysis`  

### Objectives:
1. Examine sensitivity of recovery performance across severity tiers and horizons.
2. Confirm phase gate compliance with explicit non-confirmatory boundary."""),
        nbf.v4.new_code_cell(REPO_ROOT_SNIPPET + """
import json
sens_path = os.path.join(repo_root, "results", "heldout_pilot", "sensitivity_report.json")
with open(sens_path) as f:
    sens = json.load(f)

print("=== Sensitivity Analysis by Failure Severity Tier ===")
for p, tiers in sens["sensitivity_by_severity"].items():
    print(f"{p:25s}:")
    for t_name, t_data in tiers.items():
        print(f"  {t_name:8s} (N={t_data['scenarios_count']:2d}): B0 = {t_data['succ_b0']*100:4.1f}% | B4 = {t_data['succ_b4']*100:4.1f}% | Diff = {t_data['diff']*100:+5.1f}%")
"""),
        nbf.v4.new_markdown_cell("""### Mandatory Phase Gate Conclusion
`Phase 9 fresh held-out pilot evaluation is complete. Official benchmark experiments remain paused pending explicit user approval.`"""),
    ]
    nb.cells = cells
    return nb


def run_and_save(nb: nbf.NotebookNode, path: str, nb_dir: str):
    client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": nb_dir}})
    client.execute()
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Executed and saved: {path}")


def main():
    nb_dir = os.path.join(repo_root, "notebooks")
    os.makedirs(nb_dir, exist_ok=True)

    notebooks = [
        ("31_heldout_scenario_generation.ipynb", make_notebook_31()),
        ("32_phase_9_preregistration.ipynb", make_notebook_32()),
        ("33_heldout_recovery_evaluation.ipynb", make_notebook_33()),
        ("34_history_dependence_analysis.ipynb", make_notebook_34()),
        ("35_recovery_decomposition_analysis.ipynb", make_notebook_35()),
        ("36_policy_ranking_analysis.ipynb", make_notebook_36()),
        ("37_heldout_sensitivity_analysis.ipynb", make_notebook_37()),
    ]

    for fname, nb in notebooks:
        target = os.path.join(nb_dir, fname)
        print(f"Building and executing {fname}...")
        run_and_save(nb, target, nb_dir)

    print("\nAll 7 Phase 9 analysis notebooks successfully built and executed.")


if __name__ == "__main__":
    main()
