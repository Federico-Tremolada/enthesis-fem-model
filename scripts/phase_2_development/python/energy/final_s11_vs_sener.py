"""
Script: compare_s11_sener_centerline.py
Author: FEDERICO TREMOLADA

Purpose:
Compare S11 and SENER distributions along the specimen centerline for
selected Abaqus models and generate comparison plots.

Models:
- M17
- M18
- Any additional model included in the combined CSV files with the same structure

Input:
- S11_centerline_all_models.csv
- SENER_centerline_all_models.csv

Operations:
- Load combined S11 and SENER CSV files
- Filter data for selected models
- Average duplicated x-coordinates
- Generate dual-axis plots for S11 and SENER for each model
- Generate model-to-model comparison plots for S11
- Generate model-to-model comparison plots for SENER
- Save all plots as PNG files

Output:
- M17_S11_vs_SENER.png
- M18_S11_vs_SENER.png
- Compare_S11_M17_M18.png
- Compare_SENER_M17_M18.png

Notes:
This script is intended for post-processing and visual comparison of
centerline stress and elastic strain energy density results.
Update the input file names or paths according to your own project structure.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================================
# USER SETTINGS
# =========================================

# Base folder containing the combined CSV files.
# Update this path according to your local project structure.
base_folder = os.path.join(os.getcwd(), "results_folder")

file_s11 = os.path.join(base_folder, "S11_centerline_all_models.csv")
file_sener = os.path.join(base_folder, "SENER_centerline_all_models.csv")

# =========================================
# LOAD DATA
# =========================================

df_s11 = pd.read_csv(file_s11)
df_sener = pd.read_csv(file_sener)

print("S11 columns:")
print(df_s11.columns.tolist())
print("\nSENER columns:")
print(df_sener.columns.tolist())

# =========================================
# MODEL FILTERING
# =========================================

m17_s11 = df_s11[df_s11["Model"].str.contains("M17", na=False)].copy()
m18_s11 = df_s11[df_s11["Model"].str.contains("M18", na=False)].copy()

m17_sener = df_sener[df_sener["Model"].str.contains("M17", na=False)].copy()
m18_sener = df_sener[df_sener["Model"].str.contains("M18", na=False)].copy()

# =========================================
# COLUMN NAMES
# =========================================

x_s11 = "X_centroid_mm"
y_s11 = "S11"

x_sener = "X_centroid_mm"
y_sener = "SENER"

# =========================================
# AVERAGE DUPLICATED x VALUES
# =========================================

m17_s11 = m17_s11.groupby(x_s11, as_index=False)[y_s11].mean().sort_values(by=x_s11)
m18_s11 = m18_s11.groupby(x_s11, as_index=False)[y_s11].mean().sort_values(by=x_s11)

m17_sener = m17_sener.groupby(x_sener, as_index=False)[y_sener].mean().sort_values(by=x_sener)
m18_sener = m18_sener.groupby(x_sener, as_index=False)[y_sener].mean().sort_values(by=x_sener)

# =========================================
# PLOT 1 — M17: S11 vs SENER
# =========================================

fig, ax1 = plt.subplots(figsize=(9, 5))

ax1.plot(m17_s11[x_s11], m17_s11[y_s11], 'b--o', label="S11 M17", markersize=3)
ax1.set_xlabel("x [mm]")
ax1.set_ylabel("S11 [MPa]", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(m17_sener[x_sener], m17_sener[y_sener], 'r-o', label="SENER M17", markersize=3)
ax2.set_ylabel("SENER", color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title("M17 — Comparison of S11 vs SENER along the centerline")
fig.tight_layout()
plt.savefig("M17_S11_vs_SENER.png", dpi=300)
plt.show()

# =========================================
# PLOT 2 — M18: S11 vs SENER
# =========================================

fig, ax1 = plt.subplots(figsize=(9, 5))

ax1.plot(m18_s11[x_s11], m18_s11[y_s11], 'b--o', label="S11 M18", markersize=3)
ax1.set_xlabel("x [mm]")
ax1.set_ylabel("S11 [MPa]", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(m18_sener[x_sener], m18_sener[y_sener], 'r-o', label="SENER M18", markersize=3)
ax2.set_ylabel("SENER", color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title("M18 — Comparison of S11 vs SENER along the centerline")
fig.tight_layout()
plt.savefig("M18_S11_vs_SENER.png", dpi=300)
plt.show()

# =========================================
# PLOT 3 — S11 COMPARISON: M17 vs M18
# =========================================

plt.figure(figsize=(9, 5))
plt.plot(m17_s11[x_s11], m17_s11[y_s11], 'o-', label="S11 M17", markersize=3)
plt.plot(m18_s11[x_s11], m18_s11[y_s11], 'o-', label="S11 M18", markersize=3)
plt.xlabel("x [mm]")
plt.ylabel("S11 [MPa]")
plt.title("Comparison of S11 along the centerline")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Compare_S11_M17_M18.png", dpi=300)
plt.show()

# =========================================
# PLOT 4 — SENER COMPARISON: M17 vs M18
# =========================================

plt.figure(figsize=(9, 5))
plt.plot(m17_sener[x_sener], m17_sener[y_sener], 'o-', label="SENER M17", markersize=3)
plt.plot(m18_sener[x_sener], m18_sener[y_sener], 'o-', label="SENER M18", markersize=3)
plt.xlabel("x [mm]")
plt.ylabel("SENER")
plt.title("Comparison of SENER along the centerline")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Compare_SENER_M17_M18.png", dpi=300)
plt.show()

print("\nPlots saved successfully:")
print(" - M17_S11_vs_SENER.png")
print(" - M18_S11_vs_SENER.png")
print(" - Compare_S11_M17_M18.png")
print(" - Compare_SENER_M17_M18.png")
