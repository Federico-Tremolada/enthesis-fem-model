import pandas as pd
import matplotlib.pyplot as plt

# =========================
# FILE INPUT
# =========================
file_s11 = "S11_centerline_all_models.csv"
file_sener = "SENER_centerline_all_models.csv"

# =========================
# LOAD DATA
# =========================
df_s11 = pd.read_csv(file_s11)
df_sener = pd.read_csv(file_sener)

print("Colonne S11:")
print(df_s11.columns.tolist())
print("\nColonne SENER:")
print(df_sener.columns.tolist())

# =========================
# FILTRO MODELLI
# =========================
m17_s11 = df_s11[df_s11["Model"].str.contains("M17", na=False)].copy()
m18_s11 = df_s11[df_s11["Model"].str.contains("M18", na=False)].copy()

m17_sener = df_sener[df_sener["Model"].str.contains("M17", na=False)].copy()
m18_sener = df_sener[df_sener["Model"].str.contains("M18", na=False)].copy()

# =========================
# NOMI COLONNE
# =========================
x_s11 = "X_centroid_mm"
y_s11 = "S11"

x_sener = "X_centroid_mm"
y_sener = "SENER"

# =========================
# MEDIA SU x DUPLICATI
# =========================
m17_s11 = m17_s11.groupby(x_s11, as_index=False)[y_s11].mean().sort_values(by=x_s11)
m18_s11 = m18_s11.groupby(x_s11, as_index=False)[y_s11].mean().sort_values(by=x_s11)

m17_sener = m17_sener.groupby(x_sener, as_index=False)[y_sener].mean().sort_values(by=x_sener)
m18_sener = m18_sener.groupby(x_sener, as_index=False)[y_sener].mean().sort_values(by=x_sener)

# =========================
# GRAFICO 1 — M17: S11 vs SENER
# =========================
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

plt.title("M17 — Confronto S11 vs SENER lungo la mezzeria")
fig.tight_layout()
plt.savefig("M17_S11_vs_SENER.png", dpi=300)
plt.show()

# =========================
# GRAFICO 2 — M18: S11 vs SENER
# =========================
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

plt.title("M18 — Confronto S11 vs SENER lungo la mezzeria")
fig.tight_layout()
plt.savefig("M18_S11_vs_SENER.png", dpi=300)
plt.show()

# =========================
# GRAFICO 3 — CONFRONTO S11: M17 vs M18
# =========================
plt.figure(figsize=(9, 5))
plt.plot(m17_s11[x_s11], m17_s11[y_s11], 'o-', label="S11 M17", markersize=3)
plt.plot(m18_s11[x_s11], m18_s11[y_s11], 'o-', label="S11 M18", markersize=3)
plt.xlabel("x [mm]")
plt.ylabel("S11 [MPa]")
plt.title("Confronto S11 lungo la mezzeria")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Compare_S11_M17_M18.png", dpi=300)
plt.show()

# =========================
# GRAFICO 4 — CONFRONTO SENER: M17 vs M18
# =========================
plt.figure(figsize=(9, 5))
plt.plot(m17_sener[x_sener], m17_sener[y_sener], 'o-', label="SENER M17", markersize=3)
plt.plot(m18_sener[x_sener], m18_sener[y_sener], 'o-', label="SENER M18", markersize=3)
plt.xlabel("x [mm]")
plt.ylabel("SENER")
plt.title("Confronto SENER lungo la mezzeria")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Compare_SENER_M17_M18.png", dpi=300)
plt.show()

print("\nGrafici salvati correttamente:")
print(" - M17_S11_vs_SENER.png")
print(" - M18_S11_vs_SENER.png")
print(" - Compare_S11_M17_M18.png")
print(" - Compare_SENER_M17_M18.png")