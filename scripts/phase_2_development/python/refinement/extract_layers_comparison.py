# -*- coding: utf-8 -*-
"""
Abaqus Python script
Confronto rapido modelli power-law n=2 con diverso numero di layer.

COSA FA
- Cerca automaticamente, dentro ROOT_DIR, le cartelle che contengono:
    L08, L12, L16
- Dentro ciascuna cartella cerca il file .odb
- Apre l'ODB
- Estrae dall'ultimo frame dello step scelto:
    * max von Mises
    * max S11
    * min S11
- Estrae anche il profilo S11(x) sulla mezzeria del provino
- Salva:
    1) summary_layers.csv in ./python_results/
    2) <model_name>_line.csv dentro ogni cartella modello
    3) copia dei line csv in ./python_results/line_profiles/
    4) errors_log.csv se ci sono errori

COME LANCIARE
abaqus python extract_layers_comparison.py

NOTE IMPORTANTI
- Cambia ROOT_DIR con la tua cartella principale
- Questo script usa una ricerca automatica delle cartelle, quindi
  non dipende da nomi esatti tipo PWR_n2_L08 o M10_PWR_n2_L08_v1
- Cerca cartelle che contengano nel nome:
    "L08", "L12", "L16"
"""

from odbAccess import openOdb
import os
import csv
import traceback

# ============================================================
# CONFIGURAZIONE UTENTE
# ============================================================

ROOT_DIR = r"C:\Users\fedet\OneDrive\Desktop\P01_TendonBone_Interface\II_Power_Law_Development\01_Abaqus_sims\01_FaseA_Refinement"

# Tag che identificano i modelli da confrontare
TARGET_TAGS = ["L08", "L12", "L16"]

# Se None usa automaticamente il primo step disponibile
STEP_NAME = None

# Geometria del provino: altezza = 6 mm -> mezzeria a y = 3 mm
MID_Y = 3.0
Y_TOL = 0.20

# Cartelle output
RESULTS_DIR = os.path.join(ROOT_DIR, "python_results")
LINE_DIR = os.path.join(RESULTS_DIR, "line_profiles")
SUMMARY_CSV = os.path.join(RESULTS_DIR, "summary_layers.csv")
ERROR_CSV = os.path.join(RESULTS_DIR, "errors_log.csv")

# ============================================================
# FUNZIONI UTILI
# ============================================================

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_matching_folder(root_dir, tag):
    """
    Cerca nella cartella root la prima sottocartella che contiene 'tag' nel nome.
    Esempi validi:
    - PWR_n2_L08
    - M10_PWR_n2_L08_v1
    - prova_L08_finale
    """
    candidates = []
    for name in os.listdir(root_dir):
        full = os.path.join(root_dir, name)
        if os.path.isdir(full) and tag.lower() in name.lower():
            candidates.append(full)

    if len(candidates) == 0:
        return None

    # Ordinamento semplice per avere comportamento stabile
    candidates.sort()
    return candidates[0]

def find_odb_in_folder(folder_path):
    """
    Cerca il primo file .odb nella cartella.
    """
    odbs = []
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".odb"):
            odbs.append(os.path.join(folder_path, fname))

    if not odbs:
        return None

    odbs.sort()
    return odbs[0]

def get_step_and_last_frame(odb, requested_step_name=None):
    if requested_step_name and requested_step_name in odb.steps:
        step = odb.steps[requested_step_name]
    else:
        step_names = list(odb.steps.keys())
        if not step_names:
            raise RuntimeError("Nessuno step trovato nell'ODB.")
        step = odb.steps[step_names[0]]

    if len(step.frames) == 0:
        raise RuntimeError("Nessun frame trovato nello step.")
    frame = step.frames[-1]

    return step, frame

def find_main_instance(odb):
    """
    Restituisce la prima instance disponibile.
    """
    instances = odb.rootAssembly.instances
    if not instances:
        raise RuntimeError("Nessuna instance trovata nell'assembly.")

    instance_name = list(instances.keys())[0]
    return instances[instance_name]

def get_element_centroids(instance):
    """
    Restituisce:
    dict elementLabel -> (x_centroid, y_centroid)
    """
    centroids = {}

    # Mappa nodi per accesso rapido
    node_map = {}
    for node in instance.nodes:
        node_map[node.label] = node.coordinates

    for elem in instance.elements:
        coords = []
        for node_label in elem.connectivity:
            if node_label in node_map:
                coords.append(node_map[node_label])

        if not coords:
            continue

        x_mean = sum(c[0] for c in coords) / float(len(coords))
        y_mean = sum(c[1] for c in coords) / float(len(coords))
        centroids[elem.label] = (x_mean, y_mean)

    return centroids

def extract_summary_and_line(odb_path, model_name, step_name=None):
    """
    Estrae summary globale + profilo S11(x) sulla mezzeria.
    """
    odb = None
    try:
        odb = openOdb(odb_path, readOnly=True)

        step, frame = get_step_and_last_frame(odb, step_name)
        instance = find_main_instance(odb)
        centroids = get_element_centroids(instance)

        if "S" not in frame.fieldOutputs:
            raise RuntimeError("Field output 'S' non trovato nel frame.")

        stress_field = frame.fieldOutputs["S"]

        mises_vals = []
        s11_vals = []
        line_data = []

        for val in stress_field.values:
            if not hasattr(val, "elementLabel"):
                continue

            elem_label = val.elementLabel
            if elem_label not in centroids:
                continue

            x_c, y_c = centroids[elem_label]

            # von Mises
            try:
                mises_vals.append(float(val.mises))
            except:
                pass

            # S11
            s11 = None
            try:
                s11 = float(val.data[0])
                s11_vals.append(s11)
            except:
                pass

            # Profilo sulla mezzeria
            if s11 is not None and abs(y_c - MID_Y) <= Y_TOL:
                line_data.append((x_c, s11, elem_label))

        if not mises_vals:
            raise RuntimeError("Nessun valore von Mises estratto.")
        if not s11_vals:
            raise RuntimeError("Nessun valore S11 estratto.")
        if not line_data:
            raise RuntimeError("Nessun punto trovato sulla mezzeria. Aumenta Y_TOL.")

        line_data.sort(key=lambda row: row[0])

        return {
            "model_name": model_name,
            "odb_path": odb_path,
            "step_name": step.name,
            "frame_id": frame.frameId,
            "max_mises": max(mises_vals),
            "max_s11": max(s11_vals),
            "min_s11": min(s11_vals),
            "line_data": line_data,
        }

    finally:
        if odb is not None:
            odb.close()

def write_summary_csv(summary_rows, csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model_name",
            "odb_path",
            "step_name",
            "frame_id",
            "max_mises",
            "max_s11",
            "min_s11"
        ])

        for row in summary_rows:
            writer.writerow([
                row["model_name"],
                row["odb_path"],
                row["step_name"],
                row["frame_id"],
                "{:.6f}".format(row["max_mises"]),
                "{:.6f}".format(row["max_s11"]),
                "{:.6f}".format(row["min_s11"]),
            ])

def write_line_csv(line_data, csv_path, model_name):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "S11", "element_label", "model_name"])

        for x_val, s11_val, elem_label in line_data:
            writer.writerow([
                "{:.6f}".format(x_val),
                "{:.6f}".format(s11_val),
                elem_label,
                model_name
            ])

def write_error_csv(errors, csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model_name", "error"])
        for model_name, msg in errors:
            writer.writerow([model_name, msg])

# ============================================================
# MAIN
# ============================================================

def main():
    ensure_dir(RESULTS_DIR)
    ensure_dir(LINE_DIR)

    summary_rows = []
    errors = []

    print("=" * 72)
    print("ESTRAZIONE CONFRONTO LAYER - AVVIO")
    print("ROOT_DIR = {}".format(ROOT_DIR))
    print("=" * 72)

    if not os.path.isdir(ROOT_DIR):
        print("ERRORE FATALE: ROOT_DIR non esiste.")
        print(ROOT_DIR)
        return

    for tag in TARGET_TAGS:
        print("\n--- Ricerca modello con tag: {} ---".format(tag))

        model_folder = find_matching_folder(ROOT_DIR, tag)
        if model_folder is None:
            msg = "Nessuna cartella trovata per tag '{}'".format(tag)
            print("ERRORE: " + msg)
            errors.append((tag, msg))
            continue

        model_name = os.path.basename(model_folder)
        print("Cartella trovata: {}".format(model_folder))

        odb_path = find_odb_in_folder(model_folder)
        if odb_path is None:
            msg = "Nessun file .odb trovato nella cartella '{}'".format(model_name)
            print("ERRORE: " + msg)
            errors.append((model_name, msg))
            continue

        print("ODB trovato: {}".format(os.path.basename(odb_path)))

        try:
            result = extract_summary_and_line(
                odb_path=odb_path,
                model_name=model_name,
                step_name=STEP_NAME
            )

            summary_rows.append(result)

            # CSV profilo nella cartella del modello
            model_line_csv = os.path.join(
                model_folder,
                "{}_line.csv".format(model_name)
            )
            write_line_csv(result["line_data"], model_line_csv, model_name)

            # Copia centralizzata dei profili
            central_line_csv = os.path.join(
                LINE_DIR,
                "{}_line.csv".format(model_name)
            )
            write_line_csv(result["line_data"], central_line_csv, model_name)

            print("Profilo salvato in: {}".format(model_line_csv))
            print("Copia profilo salvata in: {}".format(central_line_csv))
            print("Step      : {}".format(result["step_name"]))
            print("Frame ID  : {}".format(result["frame_id"]))
            print("Max Mises : {:.6f}".format(result["max_mises"]))
            print("Max S11   : {:.6f}".format(result["max_s11"]))
            print("Min S11   : {:.6f}".format(result["min_s11"]))
            print("N punti linea: {}".format(len(result["line_data"])))

        except Exception as e:
            msg = "Errore durante l'elaborazione: {}".format(str(e))
            print("ERRORE: " + msg)
            traceback.print_exc()
            errors.append((model_name, msg))

    if summary_rows:
        write_summary_csv(summary_rows, SUMMARY_CSV)
        print("\nSummary salvato in: {}".format(SUMMARY_CSV))
    else:
        print("\nNessun risultato valido da salvare nel summary.")

    if errors:
        write_error_csv(errors, ERROR_CSV)
        print("Error log salvato in: {}".format(ERROR_CSV))

    print("\n" + "=" * 72)
    print("ESTRAZIONE COMPLETATA")
    print("=" * 72)

if __name__ == "__main__":
    main()