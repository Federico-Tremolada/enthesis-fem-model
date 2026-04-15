# -*- coding: utf-8 -*-
# Uso:
#   abaqus python extract_energy_allse.py
#
# Cosa fa:
# 1) Cerca tutte le sottocartelle dentro base_folder
# 2) In ogni sottocartella cerca un file .odb con lo stesso nome della cartella
# 3) Estrae il valore finale di ALLSE
# 4) Salva un CSV riepilogativo
# 5) Prova anche a generare un grafico a barre PNG
#
# Struttura attesa:
# base_folder/
# ├── M17_PWR_n3_L16_nuConst_v1/
# │   └── M17_PWR_n3_L16_nuConst_v1.odb
# ├── M18_PWR_n3_L16_nuVar_v1/
# │   └── M18_PWR_n3_L16_nuVar_v1.odb

from odbAccess import openOdb
import os
import csv
import traceback

# =========================================
# USER SETTINGS
# =========================================

base_folder = r"C:\Users\fedet\OneDrive\Desktop\P01_TendonBone_Interface\II_Power_Law_Development\01_Abaqus_sims\04_FaseD_Energia_Elastica"

output_csv = os.path.join(base_folder, "energy_summary.csv")
output_png = os.path.join(base_folder, "energy_summary.png")

# Se True, cerca SOLO l'ODB con lo stesso nome della cartella
strict_same_name = True

# =========================================
# FUNCTIONS
# =========================================

def find_matching_odb(folder_path, folder_name):
    """
    Cerca il file .odb nella cartella.
    Se strict_same_name=True, cerca folder_name.odb
    Altrimenti prende il primo .odb disponibile.
    """
    expected_odb = os.path.join(folder_path, folder_name + ".odb")

    if strict_same_name:
        if os.path.isfile(expected_odb):
            return expected_odb
        return None

    # fallback: primo .odb trovato
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".odb"):
            return os.path.join(folder_path, fname)

    return None


def extract_final_allse(odb_path):
    """
    Estrae il valore finale di ALLSE dal primo step disponibile.
    Cerca ALLSE nelle history regions.
    Ritorna:
        final_allse, step_name, history_region_key
    Se non trova ALLSE, ritorna:
        None, step_name, None
    """
    odb = None
    try:
        odb = openOdb(path=odb_path, readOnly=True)

        if not odb.steps:
            return None, None, None

        # Primo step disponibile
        step_name = list(odb.steps.keys())[0]
        step = odb.steps[step_name]

        # Cerca ALLSE in tutte le history regions
        for region_key, region in step.historyRegions.items():
            if "ALLSE" in region.historyOutputs:
                data = region.historyOutputs["ALLSE"].data
                if data and len(data) > 0:
                    final_allse = data[-1][1]
                    return final_allse, step_name, region_key

        return None, step_name, None

    finally:
        if odb is not None:
            odb.close()


def save_csv(results, csv_path):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Model",
            "ODB_File",
            "Step",
            "HistoryRegion",
            "ALLSE_Final",
            "Status"
        ])
        for row in results:
            writer.writerow(row)


def make_bar_chart(results, png_path):
    """
    Grafico opzionale:
    salva un PNG con ALLSE finale per i modelli validi.
    Se matplotlib non è disponibile nell'ambiente Abaqus, salta senza errore.
    """
    valid_models = []
    valid_values = []

    for row in results:
        model_name = row[0]
        allse_value = row[4]
        status = row[5]

        if status == "OK" and allse_value is not None:
            valid_models.append(model_name)
            valid_values.append(allse_value)

    if len(valid_models) == 0:
        print("[INFO] Nessun dato valido per costruire il grafico.")
        return

    try:
        import matplotlib
        matplotlib.use("Agg")  # salva senza aprire finestre
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        plt.bar(valid_models, valid_values)
        plt.ylabel("ALLSE finale")
        plt.title("Confronto energia elastica totale (ALLSE)")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(png_path, dpi=200)
        plt.close()

        print("[OK] Grafico salvato in: {}".format(png_path))

    except Exception as e:
        print("[WARNING] Impossibile creare il grafico PNG.")
        print("Motivo: {}".format(str(e)))


# =========================================
# MAIN
# =========================================

def main():
    print("=" * 60)
    print("ESTRAZIONE AUTOMATICA ALLSE DA FILE ODB")
    print("=" * 60)
    print("Cartella base: {}".format(base_folder))
    print("CSV output   : {}".format(output_csv))
    print("PNG output   : {}".format(output_png))
    print("")

    if not os.path.isdir(base_folder):
        print("[ERRORE] La cartella base non esiste.")
        return

    results = []

    subfolders = [
        name for name in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, name))
    ]

    if len(subfolders) == 0:
        print("[ERRORE] Nessuna sottocartella trovata nella cartella base.")
        return

    for folder_name in sorted(subfolders):
        folder_path = os.path.join(base_folder, folder_name)
        print("-" * 60)
        print("Modello: {}".format(folder_name))

        odb_path = find_matching_odb(folder_path, folder_name)

        if odb_path is None:
            print("[WARNING] Nessun file .odb trovato con nome uguale alla cartella.")
            results.append([
                folder_name,
                "",
                "",
                "",
                None,
                "ODB_NOT_FOUND"
            ])
            continue

        print("ODB trovato: {}".format(os.path.basename(odb_path)))

        try:
            final_allse, step_name, region_key = extract_final_allse(odb_path)

            if final_allse is None:
                print("[WARNING] ALLSE non trovato nelle history outputs.")
                results.append([
                    folder_name,
                    os.path.basename(odb_path),
                    step_name if step_name else "",
                    "",
                    None,
                    "ALLSE_NOT_FOUND"
                ])
            else:
                print("[OK] Step         : {}".format(step_name))
                print("[OK] HistoryRegion: {}".format(region_key))
                print("[OK] ALLSE finale : {}".format(final_allse))

                results.append([
                    folder_name,
                    os.path.basename(odb_path),
                    step_name,
                    region_key,
                    final_allse,
                    "OK"
                ])

        except Exception as e:
            print("[ERRORE] Fallita lettura del file ODB.")
            print(str(e))
            traceback.print_exc()

            results.append([
                folder_name,
                os.path.basename(odb_path),
                "",
                "",
                None,
                "READ_ERROR"
            ])

    print("")
    print("=" * 60)
    print("SALVATAGGIO RISULTATI")
    print("=" * 60)

    save_csv(results, output_csv)
    print("[OK] CSV salvato in: {}".format(output_csv))

    make_bar_chart(results, output_png)

    print("")
    print("=" * 60)
    print("FINE")
    print("=" * 60)


if __name__ == "__main__":
    main()