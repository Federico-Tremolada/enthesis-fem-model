# -*- coding: utf-8 -*-
# Uso:
#   abaqus python extract_sener_centerline.py
#
# Cosa fa:
# 1) Cerca solo le sottocartelle che finiscono con "_sener"
# 2) In ciascuna cartella cerca il file .odb
# 3) Apre l'ultimo frame del primo step
# 4) Estrae SENER sugli elementi vicini alla mezzeria
# 5) Salva un CSV per ogni modello
# 6) Salva un CSV combinato
# 7) Genera un grafico PNG di confronto

from odbAccess import openOdb
from abaqusConstants import INTEGRATION_POINT
import os
import csv
import traceback

# =========================================================
# USER SETTINGS
# =========================================================

base_folder = os.getcwd()   # cartella da cui lanci lo script

# Mezzeria del provino
y_target = 3.0      # mm
y_tol = 0.20        # tolleranza attorno alla mezzeria

# Se None, usa automaticamente la prima instance trovata
target_instance_name = None

combined_csv = os.path.join(base_folder, "SENER_centerline_all_models.csv")
combined_png = os.path.join(base_folder, "SENER_centerline_comparison.png")

# =========================================================
# FUNZIONI UTILI
# =========================================================

def find_odb_in_folder(folder_path):
    odb_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".odb")]
    if len(odb_files) == 0:
        return None
    if len(odb_files) == 1:
        return os.path.join(folder_path, odb_files[0])

    folder_name = os.path.basename(folder_path).lower()
    for f in odb_files:
        if os.path.splitext(f)[0].lower() == folder_name:
            return os.path.join(folder_path, f)

    return os.path.join(folder_path, odb_files[0])


def get_first_step_and_last_frame(odb):
    if not odb.steps:
        return None, None, None
    step_name = list(odb.steps.keys())[0]
    step = odb.steps[step_name]
    if len(step.frames) == 0:
        return step_name, step, None
    frame = step.frames[-1]
    return step_name, step, frame


def choose_instance(odb):
    asm = odb.rootAssembly

    if target_instance_name is not None:
        if target_instance_name in asm.instances:
            return asm.instances[target_instance_name]
        raise ValueError("Instance '{}' non trovata nell'odb.".format(target_instance_name))

    instance_names = list(asm.instances.keys())
    if len(instance_names) == 0:
        raise ValueError("Nessuna instance trovata nell'odb.")

    return asm.instances[instance_names[0]]


def build_node_dict(instance):
    node_dict = {}
    for node in instance.nodes:
        node_dict[node.label] = node.coordinates
    return node_dict


def element_centroid_2d(elem, node_dict):
    xs = []
    ys = []
    for nlabel in elem.connectivity:
        coords = node_dict[nlabel]
        xs.append(coords[0])
        ys.append(coords[1])
    x_c = sum(xs) / float(len(xs))
    y_c = sum(ys) / float(len(ys))
    return x_c, y_c


def extract_sener_by_element(frame, instance):
    """
    Restituisce un dizionario:
    elementLabel -> valore medio di SENER su tutti gli integration points dell'elemento
    """
    if "SENER" not in frame.fieldOutputs:
        return None

    sener_field = frame.fieldOutputs["SENER"]
    sener_sub = sener_field.getSubset(region=instance, position=INTEGRATION_POINT)

    elem_vals = {}

    for v in sener_sub.values:
        el = v.elementLabel
        data = v.data

        if isinstance(data, (tuple, list)):
            val = float(data[0])
        else:
            val = float(data)

        if el not in elem_vals:
            elem_vals[el] = []
        elem_vals[el].append(val)

    elem_avg = {}
    for el, vals in elem_vals.items():
        elem_avg[el] = sum(vals) / float(len(vals))

    return elem_avg


def clean_model_name(folder_name):
    if folder_name.lower().endswith("_sener"):
        return folder_name[:-6]
    return folder_name


def save_model_csv(csv_path, rows):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Model", "ElementLabel", "X_centroid_mm", "Y_centroid_mm", "SENER"])
        writer.writerows(rows)


def save_combined_csv(csv_path, rows):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Model", "ElementLabel", "X_centroid_mm", "Y_centroid_mm", "SENER"])
        writer.writerows(rows)


def make_comparison_plot(rows, png_path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        by_model = {}
        for r in rows:
            model = r[0]
            x = r[2]
            sener = r[4]
            if model not in by_model:
                by_model[model] = []
            by_model[model].append((x, sener))

        plt.figure(figsize=(10, 6))

        for model, pts in sorted(by_model.items()):
            pts_sorted = sorted(pts, key=lambda t: t[0])
            xs = [p[0] for p in pts_sorted]
            ys = [p[1] for p in pts_sorted]
            plt.plot(xs, ys, marker="o", markersize=3, linewidth=1.2, label=model)

        plt.xlabel("x sulla mezzeria [mm]")
        plt.ylabel("SENER")
        plt.title("Confronto SENER lungo la mezzeria")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_path, dpi=200)
        plt.close()

        print("[OK] Grafico salvato in: {}".format(png_path))

    except Exception as e:
        print("[WARNING] Impossibile creare il grafico.")
        print("Motivo: {}".format(str(e)))


# =========================================================
# MAIN
# =========================================================

def main():
    print("=" * 70)
    print("ESTRAZIONE SENER LUNGO LA MEZZERIA")
    print("=" * 70)
    print("Cartella base : {}".format(base_folder))
    print("y_target      : {}".format(y_target))
    print("y_tol         : {}".format(y_tol))
    print("")

    if not os.path.isdir(base_folder):
        print("[ERRORE] La cartella base non esiste.")
        return

    subfolders = [
        name for name in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, name)) and name.lower().endswith("_sener")
    ]

    if len(subfolders) == 0:
        print("[ERRORE] Nessuna sottocartella *_sener trovata.")
        return

    combined_rows = []

    for folder_name in sorted(subfolders):
        folder_path = os.path.join(base_folder, folder_name)
        odb_path = find_odb_in_folder(folder_path)

        print("-" * 70)
        print("Cartella sorgente: {}".format(folder_name))

        if odb_path is None:
            print("[WARNING] Nessun ODB trovato: salto.")
            continue

        model_name = clean_model_name(folder_name)

        print("Modello        : {}".format(model_name))
        print("ODB            : {}".format(os.path.basename(odb_path)))

        odb = None
        try:
            odb = openOdb(path=odb_path, readOnly=True)

            step_name, step, frame = get_first_step_and_last_frame(odb)
            if frame is None:
                print("[WARNING] Nessun frame disponibile.")
                odb.close()
                continue

            print("Step usato     : {}".format(step_name))
            print("Frame usato    : ultimo")

            instance = choose_instance(odb)
            print("Instance usata : {}".format(instance.name))

            node_dict = build_node_dict(instance)
            sener_by_elem = extract_sener_by_element(frame, instance)

            if sener_by_elem is None:
                print("[WARNING] SENER non presente nel field output.")
                odb.close()
                continue

            model_rows = []

            for elem in instance.elements:
                elabel = elem.label

                if elabel not in sener_by_elem:
                    continue

                x_c, y_c = element_centroid_2d(elem, node_dict)

                if abs(y_c - y_target) <= y_tol:
                    row = [model_name, elabel, x_c, y_c, sener_by_elem[elabel]]
                    model_rows.append(row)
                    combined_rows.append(row)

            odb.close()

            if len(model_rows) == 0:
                print("[WARNING] Nessun elemento trovato vicino alla mezzeria.")
                continue

            model_rows = sorted(model_rows, key=lambda r: r[2])

            out_csv = os.path.join(folder_path, model_name + "_SENER_centerline.csv")
            save_model_csv(out_csv, model_rows)

            print("[OK] Elementi estratti : {}".format(len(model_rows)))
            print("[OK] CSV modello      : {}".format(out_csv))

        except Exception as e:
            print("[ERRORE] Problema durante l'estrazione.")
            print(str(e))
            traceback.print_exc()
            if odb is not None:
                try:
                    odb.close()
                except:
                    pass

    print("")
    print("=" * 70)
    print("SALVATAGGIO FINALE")
    print("=" * 70)

    if len(combined_rows) == 0:
        print("[WARNING] Nessun dato complessivo disponibile.")
        return

    combined_rows = sorted(combined_rows, key=lambda r: (r[0], r[2]))
    save_combined_csv(combined_csv, combined_rows)
    print("[OK] CSV combinato salvato in: {}".format(combined_csv))

    make_comparison_plot(combined_rows, combined_png)

    print("")
    print("=" * 70)
    print("FINE")
    print("=" * 70)


if __name__ == "__main__":
    main()