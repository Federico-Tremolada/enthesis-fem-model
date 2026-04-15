"""
Script: compare_s11_all_models.py
Author: FEDERICO TREMOLADA

Purpose:
Perform comparative analysis of S11 stress distributions across multiple
FEM models of the tendon-bone interface.

Models:
- Sharp
- Linear
- Exponential
- Power n=0.5
- Power n=2
- Any additional model structured in the same way

Input:
- CSV files containing:
    x   -> coordinate along the interface [mm]
    S11 -> longitudinal stress [MPa]

Operations:
- Load S11(x) data from multiple model CSV files
- Normalize the spatial coordinate using a reference model length
- Compute summary metrics for each model
- Generate a full comparative S11 plot
- Generate a zoomed comparative plot near the interface region
- Save the metrics and figures for further analysis

Output:
- summary_metrics_all.csv
- S11_all_models.png
- S11_zoom_all_models.png

Notes:
This script is intended for comparative post-processing of S11 distributions
across different material transition laws.
All models should share the same geometry and coordinate system.
Update the base_folder variable according to your own project structure.
Run this script with standard Python, not Abaqus Python.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================================
# USER SETTINGS
# =========================================

# Base folder containing the CSV input files.
# Update this path according to your local project structure.
base_folder = os.path.join(os.getcwd(), "results_folder")

files = {
    "Sharp": os.path.join(base_folder, "M01_sharp_v1_line.csv"),
    "Linear": os.path.join(base_folder, "M02_linear_v1_line.csv"),
    "Exponential": os.path.join(base_folder, "M03_exponential_v1_line.csv"),
    "Power n=0.5": os.path.join(base_folder, "M04_power_n05_v1_line.csv"),
    "Power n=2": os.path.join(base_folder, "M05_power_n2_v1_line.csv"),
}

summary_metrics_csv = os.path.join(base_folder, "summary_metrics_all.csv")
plot_all_png = os.path.join(base_folder, "S11_all_models.png")
plot_zoom_png = os.path.join(base_folder, "S11_zoom_all_models.png")

# =========================================
# LOAD DATA
# =========================================

data = {}

for label, filename in files.items():
    df = pd.read_csv(filename)
    data[label] = df

# =========================================
# X NORMALIZATION
# Use the first model length as reference
# =========================================

reference_label = list(data.keys())[0]
L = data[reference_label]["x"].max()

for label in data:
    data[label]["x_norm"] = data[label]["x"] / L

# =========================================
# METRICS
# =========================================

def compute_metrics(df, name):
    max_s11 = df["S11"].max()
    min_s11 = df["S11"].min()
    x_at_max = df.loc[df["S11"].idxmax(), "x"]
    xnorm_at_max = df.loc[df["S11"].idxmax(), "x_norm"]
    mean_s11 = df["S11"].mean()

    return {
        "model": name,
        "max_S11": max_s11,
        "min_S11": min_s11,
        "x_at_max": x_at_max,
        "xnorm_at_max": xnorm_at_max,
        "mean_S11": mean_s11
    }

metrics = []

for label, df in data.items():
    metrics.append(compute_metrics(df, label))

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv(summary_metrics_csv, index=False)

print("\n=== METRICS ===")
print(metrics_df)

# =========================================
# PLOT STYLE
# =========================================

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.linewidth": 1.2,
    "grid.color": "#d0d0d0",
    "grid.linestyle": "-",
    "grid.linewidth": 0.8,
    "font.size": 12,
})

styles = {
    "Sharp": {"marker": "o", "linewidth": 2.7},
    "Linear": {"marker": "s", "linewidth": 2.7},
    "Exponential": {"marker": "^", "linewidth": 2.7},
    "Power n=0.5": {"marker": "D", "linewidth": 2.7},
    "Power n=2": {"marker": "v", "linewidth": 2.7},
}

# =========================================
# FULL COMPARISON PLOT
# =========================================

fig, ax = plt.subplots(figsize=(10, 6.5))

for label, df in data.items():
    ax.plot(
        df["x_norm"],
        df["S11"],
        label=label,
        linewidth=styles[label]["linewidth"],
        marker=styles[label]["marker"],
        markersize=4
    )

ax.set_xlabel("Normalized position")
ax.set_ylabel("S11 (MPa)")
ax.grid(True)
ax.legend(frameon=False, ncol=2)

fig.tight_layout()
fig.savefig(plot_all_png, dpi=300, bbox_inches="tight")

# =========================================
# INTERFACE ZOOM PLOT
# =========================================

xmin, xmax = 0.42, 0.60

fig, ax = plt.subplots(figsize=(10, 6.5))

for label, df in data.items():
    df_zoom = df[(df["x_norm"] >= xmin) & (df["x_norm"] <= xmax)]

    ax.plot(
        df_zoom["x_norm"],
        df_zoom["S11"],
        label=label,
        linewidth=styles[label]["linewidth"],
        marker=styles[label]["marker"],
        markersize=5
    )

ax.set_xlabel("Normalized position")
ax.set_ylabel("S11 (MPa)")
ax.grid(True)
ax.legend(frameon=False, ncol=2)

fig.tight_layout()
fig.savefig(plot_zoom_png, dpi=300, bbox_inches="tight")

plt.show()
