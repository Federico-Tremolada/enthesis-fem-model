import pandas as pd
import matplotlib.pyplot as plt

# ======================
# FILE CSV
# ======================
files = {
    "Sharp": "M01_sharp_v1_line.csv",
    "Linear": "M02_linear_v1_line.csv",
    "Exponential": "M03_exponential_v1_line.csv",
    "Power n=0.5": "M04_power_n05_v1_line.csv",
    "Power n=2": "M05_power_n2_v1_line.csv",
}

# ======================
# LOAD DATI
# ======================
data = {}

for label, filename in files.items():
    df = pd.read_csv(filename)
    data[label] = df

# ======================
# NORMALIZZAZIONE X
# uso la lunghezza del primo modello come riferimento
# ======================
reference_label = list(data.keys())[0]
L = data[reference_label]["x"].max()

for label in data:
    data[label]["x_norm"] = data[label]["x"] / L

# ======================
# METRICHE
# ======================
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
metrics_df.to_csv("summary_metrics_all.csv", index=False)

print("\n=== METRICS ===")
print(metrics_df)

# ======================
# STILE GRAFICO
# ======================
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

# ======================
# GRAFICO COMPLETO
# ======================
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
fig.savefig("S11_all_models.png", dpi=300, bbox_inches="tight")

# ======================
# ZOOM INTERFACCIA
# ======================
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
fig.savefig("S11_zoom_all_models.png", dpi=300, bbox_inches="tight")

plt.show()