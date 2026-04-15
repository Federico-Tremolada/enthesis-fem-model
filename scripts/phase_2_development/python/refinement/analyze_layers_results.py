"""
Script: analyze_layer_results.py
Author: FEDERICO TREMOLADA

Purpose:
Perform a rapid comparison of layer-refinement results by reading summary
metrics and S11 centerline profiles, then generating quantitative and
graphical outputs.

Models:
- L08
- L12
- L16
- Any additional model following the same naming convention

Input:
- python_results/summary_layers.csv
- python_results/line_profiles/*_line.csv

Operations:
- Load summary_layers.csv
- Load S11(x) line profiles
- Generate a comparative S11 plot
- Compute percentage differences between L08, L12, and L16
- Write a preliminary automatic convergence report

Output:
- python_results/comparison_metrics.csv
- python_results/convergence_report.txt
- python_results/S11_layers_comparison.png

Notes:
This script is intended for rapid post-processing of Phase A layer-refinement
results.
Update the root_dir variable according to your own project structure.
Run this script with standard Python, not Abaqus Python.
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# =========================================
# USER SETTINGS
# =========================================

# Root folder containing the python_results directory.
# Update this path according to your local project structure.
root_dir = os.path.join(os.getcwd(), "project_root")

results_dir = os.path.join(root_dir, "python_results")
line_dir = os.path.join(results_dir, "line_profiles")

summary_csv = os.path.join(results_dir, "summary_layers.csv")
metrics_csv = os.path.join(results_dir, "comparison_metrics.csv")
report_txt = os.path.join(results_dir, "convergence_report.txt")
plot_png = os.path.join(results_dir, "S11_layers_comparison.png")

target_tags = ["L08", "L12", "L16"]

# Practical threshold to consider two results "almost equal"
# in percentage terms
convergence_threshold_percent = 3.0

# =========================================
# UTILITY FUNCTIONS
# =========================================

def percent_change(old, new):
    if old == 0:
        return None
    return 100.0 * (new - old) / abs(old)

def abs_percent_change(a, b):
    if a == 0:
        return None
    return 100.0 * abs(b - a) / abs(a)

def detect_tag(name):
    name_low = name.lower()
    for tag in target_tags:
        if tag.lower() in name_low:
            return tag
    return None

def load_summary(summary_csv):
    if not os.path.exists(summary_csv):
        raise FileNotFoundError("summary_layers.csv not found: {}".format(summary_csv))

    df = pd.read_csv(summary_csv)

    if df.empty:
        raise RuntimeError("summary_layers.csv is empty.")

    df["tag"] = df["model_name"].apply(detect_tag)
    df = df[df["tag"].notna()].copy()

    if df.empty:
        raise RuntimeError("No L08/L12/L16 models found in the summary.")

    # Keep only one record per tag
    df = df.drop_duplicates(subset=["tag"], keep="first")

    return df

def load_line_profiles(line_dir):
    if not os.path.isdir(line_dir):
        raise FileNotFoundError("line_profiles folder not found: {}".format(line_dir))

    profiles = {}

    csv_files = glob.glob(os.path.join(line_dir, "*.csv"))
    if not csv_files:
        raise RuntimeError("No line CSV files found in {}".format(line_dir))

    for csv_path in csv_files:
        fname = os.path.basename(csv_path)
        tag = detect_tag(fname)
        if tag is None:
            continue

        df = pd.read_csv(csv_path)
        if "x" not in df.columns or "S11" not in df.columns:
            continue

        df = df.sort_values(by="x").reset_index(drop=True)
        profiles[tag] = {
            "path": csv_path,
            "data": df
        }

    return profiles

def compute_metrics(summary_df):
    """
    Build two tables:
    - absolute values
    - percentage differences between consecutive refinement levels
    """
    summary_df = summary_df.set_index("tag")

    required = ["L08", "L12", "L16"]
    available = [tag for tag in required if tag in summary_df.index]

    rows = []

    for tag in available:
        rows.append({
            "tag": tag,
            "model_name": summary_df.loc[tag, "model_name"],
            "max_mises": float(summary_df.loc[tag, "max_mises"]),
            "max_s11": float(summary_df.loc[tag, "max_s11"]),
            "min_s11": float(summary_df.loc[tag, "min_s11"]),
        })

    metrics_df = pd.DataFrame(rows)

    # Percentage differences for consecutive pairs
    pair_rows = []
    pairs = [("L08", "L12"), ("L12", "L16"), ("L08", "L16")]

    for a, b in pairs:
        if a in summary_df.index and b in summary_df.index:
            max_mises_a = float(summary_df.loc[a, "max_mises"])
            max_mises_b = float(summary_df.loc[b, "max_mises"])

            max_s11_a = float(summary_df.loc[a, "max_s11"])
            max_s11_b = float(summary_df.loc[b, "max_s11"])

            min_s11_a = float(summary_df.loc[a, "min_s11"])
            min_s11_b = float(summary_df.loc[b, "min_s11"])

            pair_rows.append({
                "comparison": "{} -> {}".format(a, b),
                "delta_max_mises_percent_abs": abs_percent_change(max_mises_a, max_mises_b),
                "delta_max_s11_percent_abs": abs_percent_change(max_s11_a, max_s11_b),
                "delta_min_s11_percent_abs": abs_percent_change(min_s11_a, min_s11_b),
            })

    pair_df = pd.DataFrame(pair_rows)

    return metrics_df, pair_df

def make_plot(profiles, out_png):
    plt.figure(figsize=(10, 6))

    plotting_order = ["L08", "L12", "L16"]

    for tag in plotting_order:
        if tag in profiles:
            df = profiles[tag]["data"]
            plt.plot(df["x"], df["S11"], label=tag)

    plt.xlabel("x [mm]")
    plt.ylabel("S11 [MPa]")
    plt.title("Comparison of S11(x) profiles - layer refinement")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def write_report(summary_df, pair_df, report_txt):
    summary_df = summary_df.set_index("tag")

    def get_value(tag, column):
        if tag in summary_df.index:
            return float(summary_df.loc[tag, column])
        return None

    max_mises_08 = get_value("L08", "max_mises")
    max_mises_12 = get_value("L12", "max_mises")
    max_mises_16 = get_value("L16", "max_mises")

    max_s11_08 = get_value("L08", "max_s11")
    max_s11_12 = get_value("L12", "max_s11")
    max_s11_16 = get_value("L16", "max_s11")

    min_s11_08 = get_value("L08", "min_s11")
    min_s11_12 = get_value("L12", "min_s11")
    min_s11_16 = get_value("L16", "min_s11")

    def get_pair(comp, col):
        sub = pair_df[pair_df["comparison"] == comp]
        if sub.empty:
            return None
        return float(sub.iloc[0][col])

    d_mises_12_16 = get_pair("L12 -> L16", "delta_max_mises_percent_abs")
    d_maxs11_12_16 = get_pair("L12 -> L16", "delta_max_s11_percent_abs")
    d_mins11_12_16 = get_pair("L12 -> L16", "delta_min_s11_percent_abs")

    conclusions = []

    if (
        d_mises_12_16 is not None and
        d_maxs11_12_16 is not None and
        d_mins11_12_16 is not None
    ):
        if (
            d_mises_12_16 < convergence_threshold_percent and
            d_maxs11_12_16 < convergence_threshold_percent and
            d_mins11_12_16 < convergence_threshold_percent
        ):
            conclusions.append(
                "The L12 -> L16 comparison shows variations below the {:.1f}% threshold "
                "for max von Mises, max S11, and min S11. "
                "This suggests substantial convergence with respect to the number of layers.".format(
                    convergence_threshold_percent
                )
            )
            conclusions.append(
                "Preliminary conclusion: Phase A can be considered complete "
                "and the study can proceed to the sensitivity analysis on exponent n."
            )
        else:
            conclusions.append(
                "The L12 -> L16 comparison still shows non-negligible variations "
                "in at least one of the main scalar metrics."
            )
            conclusions.append(
                "Preliminary conclusion: convergence is not yet fully demonstrated "
                "by scalar values alone; the S11(x) plot should also be checked."
            )
    else:
        conclusions.append(
            "Automatic evaluation of the L12 -> L16 comparison could not be completed."
        )

    lines = []
    lines.append("CONVERGENCE REPORT - PHASE A")
    lines.append("=" * 50)
    lines.append("")

    lines.append("EXTRACTED VALUES")
    lines.append("-" * 50)
    for tag in ["L08", "L12", "L16"]:
        if tag in summary_df.index:
            lines.append(
                "{} | model = {} | max Mises = {:.6f} | max S11 = {:.6f} | min S11 = {:.6f}".format(
                    tag,
                    summary_df.loc[tag, "model_name"],
                    float(summary_df.loc[tag, "max_mises"]),
                    float(summary_df.loc[tag, "max_s11"]),
                    float(summary_df.loc[tag, "min_s11"]),
                )
            )

    lines.append("")
    lines.append("ABSOLUTE PERCENT DIFFERENCES")
    lines.append("-" * 50)

    for _, row in pair_df.iterrows():
        lines.append(
            "{} | Δ max Mises = {:.4f}% | Δ max S11 = {:.4f}% | Δ min S11 = {:.4f}%".format(
                row["comparison"],
                row["delta_max_mises_percent_abs"],
                row["delta_max_s11_percent_abs"],
                row["delta_min_s11_percent_abs"],
            )
        )

    lines.append("")
    lines.append("AUTOMATIC CONCLUSIONS")
    lines.append("-" * 50)
    for c in conclusions:
        lines.append(c)

    with open(report_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================
# MAIN
# =========================================

def main():
    print("=" * 70)
    print("LAYER RESULTS ANALYSIS - START")
    print("=" * 70)

    if not os.path.isdir(root_dir):
        raise FileNotFoundError("root_dir not found: {}".format(root_dir))

    if not os.path.isdir(results_dir):
        raise FileNotFoundError("python_results not found: {}".format(results_dir))

    summary_df = load_summary(summary_csv)
    profiles = load_line_profiles(line_dir)

    metrics_df, pair_df = compute_metrics(summary_df)

    metrics_df.to_csv(metrics_csv, index=False)
    make_plot(profiles, plot_png)
    write_report(summary_df, pair_df, report_txt)

    print("Summary loaded from    : {}".format(summary_csv))
    print("Profiles loaded from   : {}".format(line_dir))
    print("Metrics saved to       : {}".format(metrics_csv))
    print("Plot saved to          : {}".format(plot_png))
    print("Report saved to        : {}".format(report_txt))
    print("")
    print("ANALYSIS COMPLETED")

if __name__ == "__main__":
    main()
