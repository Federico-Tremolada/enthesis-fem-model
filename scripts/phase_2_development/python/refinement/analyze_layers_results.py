# -*- coding: utf-8 -*-
"""
Analisi rapida dei risultati dei modelli:
- L08
- L12
- L16

INPUT ATTESI
ROOT_DIR/
└── python_results/
    ├── summary_layers.csv
    └── line_profiles/
        ├── ...L08..._line.csv
        ├── ...L12..._line.csv
        └── ...L16..._line.csv

OUTPUT
ROOT_DIR/
└── python_results/
    ├── comparison_metrics.csv
    ├── convergence_report.txt
    └── S11_layers_comparison.png

COSA FA
1) legge summary_layers.csv
2) legge i profili S11(x)
3) genera grafico comparativo
4) calcola differenze percentuali tra L08, L12, L16
5) scrive una conclusione automatica preliminare

NOTE
- Cambia ROOT_DIR con il tuo percorso
- Questo script va lanciato con Python normale, non Abaqus Python
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURAZIONE UTENTE
# ============================================================

ROOT_DIR = r"C:\Users\fedet\OneDrive\Desktop\P01_TendonBone_Interface\II_Power_Law_Development\01_Abaqus_sims\01_FaseA_Refinement"

RESULTS_DIR = os.path.join(ROOT_DIR, "python_results")
LINE_DIR = os.path.join(RESULTS_DIR, "line_profiles")

SUMMARY_CSV = os.path.join(RESULTS_DIR, "summary_layers.csv")
METRICS_CSV = os.path.join(RESULTS_DIR, "comparison_metrics.csv")
REPORT_TXT = os.path.join(RESULTS_DIR, "convergence_report.txt")
PLOT_PNG = os.path.join(RESULTS_DIR, "S11_layers_comparison.png")

TARGET_TAGS = ["L08", "L12", "L16"]

# Soglia pratica per dire che due risultati sono "quasi uguali"
# in termini percentuali
CONVERGENCE_THRESHOLD_PERCENT = 3.0

# ============================================================
# FUNZIONI UTILI
# ============================================================

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
    for tag in TARGET_TAGS:
        if tag.lower() in name_low:
            return tag
    return None

def load_summary(summary_csv):
    if not os.path.exists(summary_csv):
        raise FileNotFoundError("summary_layers.csv non trovato: {}".format(summary_csv))

    df = pd.read_csv(summary_csv)

    if df.empty:
        raise RuntimeError("summary_layers.csv è vuoto.")

    df["tag"] = df["model_name"].apply(detect_tag)
    df = df[df["tag"].notna()].copy()

    if df.empty:
        raise RuntimeError("Nessun modello L08/L12/L16 trovato nel summary.")

    # Teniamo un solo record per tag
    df = df.drop_duplicates(subset=["tag"], keep="first")

    return df

def load_line_profiles(line_dir):
    if not os.path.isdir(line_dir):
        raise FileNotFoundError("Cartella line_profiles non trovata: {}".format(line_dir))

    profiles = {}

    csv_files = glob.glob(os.path.join(line_dir, "*.csv"))
    if not csv_files:
        raise RuntimeError("Nessun line csv trovato in {}".format(line_dir))

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
    Costruisce una tabella con:
    - valori assoluti
    - differenze percentuali tra livelli successivi
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

    # differenze percentuali su coppie consecutive
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
    plt.title("Confronto profili S11(x) - layer refinement")
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
            d_mises_12_16 < CONVERGENCE_THRESHOLD_PERCENT and
            d_maxs11_12_16 < CONVERGENCE_THRESHOLD_PERCENT and
            d_mins11_12_16 < CONVERGENCE_THRESHOLD_PERCENT
        ):
            conclusions.append(
                "Il confronto L12 -> L16 mostra variazioni inferiori alla soglia del "
                "{:.1f}% per max von Mises, max S11 e min S11. "
                "Questo suggerisce una sostanziale convergenza rispetto al numero di layer.".format(
                    CONVERGENCE_THRESHOLD_PERCENT
                )
            )
            conclusions.append(
                "Conclusione preliminare: la Fase A può essere considerata chiusa "
                "e si può passare alla sensitivity analysis sull'esponente n."
            )
        else:
            conclusions.append(
                "Il confronto L12 -> L16 mostra variazioni ancora non trascurabili "
                "in almeno una delle metriche principali."
            )
            conclusions.append(
                "Conclusione preliminare: la convergenza non è ancora pienamente dimostrata "
                "solo dai valori scalari; conviene verificare anche il grafico S11(x)."
            )
    else:
        conclusions.append(
            "Non è stato possibile valutare automaticamente il confronto L12 -> L16."
        )

    lines = []
    lines.append("REPORT DI CONVERGENZA - FASE A")
    lines.append("=" * 50)
    lines.append("")

    lines.append("VALORI ESTRATTI")
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
    lines.append("DIFFERENZE PERCENTUALI ASSOLUTE")
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
    lines.append("CONCLUSIONI AUTOMATICHE")
    lines.append("-" * 50)
    for c in conclusions:
        lines.append(c)

    with open(report_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("ANALISI RISULTATI LAYER - AVVIO")
    print("=" * 70)

    if not os.path.isdir(ROOT_DIR):
        raise FileNotFoundError("ROOT_DIR non trovato: {}".format(ROOT_DIR))

    if not os.path.isdir(RESULTS_DIR):
        raise FileNotFoundError("python_results non trovato: {}".format(RESULTS_DIR))

    summary_df = load_summary(SUMMARY_CSV)
    profiles = load_line_profiles(LINE_DIR)

    metrics_df, pair_df = compute_metrics(summary_df)

    metrics_df.to_csv(METRICS_CSV, index=False)
    make_plot(profiles, PLOT_PNG)
    write_report(summary_df, pair_df, REPORT_TXT)

    print("Summary letto da       : {}".format(SUMMARY_CSV))
    print("Profili letti da       : {}".format(LINE_DIR))
    print("Metriche salvate in    : {}".format(METRICS_CSV))
    print("Grafico salvato in     : {}".format(PLOT_PNG))
    print("Report salvato in      : {}".format(REPORT_TXT))
    print("")
    print("ANALISI COMPLETATA")

if __name__ == "__main__":
    main()