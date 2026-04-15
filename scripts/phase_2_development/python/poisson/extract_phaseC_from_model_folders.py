# -*- coding: utf-8 -*-
# Abaqus Python script
# Estrazione risultati Fase C:
# - max von Mises
# - max S11
# - min S11
# - coordinate dei picchi
# - profilo lungo la mezzeria y = 3.0 mm
#
# Struttura attesa:
# cartella_progetto/
#   M17_PWR_n3_L16_nuConst_v1/
#       *.odb
#   M18_PWR_n3_L16_nuVar_v1/
#       *.odb
#   python/
#       extract_phaseC_from_model_folders.py
#
# Output:
# cartella_progetto/
#   results_summary/
#       summary_phaseC.csv
#       line_profiles_phaseC/
#           M17_..._line.csv
#           M18_..._line.csv

from odbAccess import openOdb
from abaqusConstants import *
import os
import csv
import traceback

# ============================================================
# PARAMETRI UTENTE
# ============================================================

Y_TARGET = 3.0
Y_TOL = 0.25

MODEL_FOLDERS = [
    "M17_PWR_n3_L16_nuConst_v1",
    "M18_PWR_n3_L16_nuVar_v1",
]

PREFERRED_STEP = "Step-1"

# ============================================================
# FUNZIONI BASE
# ============================================================

def safe_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def mean(values):
    if len(values) == 0:
        return None
    return sum(values) / float(len(values))

def find_project_root():
    return os.getcwd()

def list_model_folders(project_root):
    model_names = []

    if len(MODEL_FOLDERS) > 0:
        for name in MODEL_FOLDERS:
            full = os.path.join(project_root, name)
            if os.path.isdir(full):
                model_names.append(name)
            else:
                print("ATTENZIONE: cartella non trovata -> %s" % full)
        return model_names

    items = os.listdir(project_root)
    for item in items:
        full = os.path.join(project_root, item)

        if not os.path.isdir(full):
            continue

        if item.lower() in ["python", "matlab", "results_summary"]:
            continue

        if item.endswith(".simdir"):
            continue

        if not item.startswith("M"):
            continue

        has_odb = False
        subfiles = os.listdir(full)
        for f in subfiles:
            if f.lower().endswith(".odb"):
                has_odb = True
                break

        if has_odb:
            model_names.append(item)

    model_names.sort()
    return model_names

def find_odb_in_folder(folder_path):
    odb_files = []
    for f in os.listdir(folder_path):
        if f.lower().endswith(".odb"):
            odb_files.append(f)

    if len(odb_files) == 0:
        return None

    if len(odb_files) == 1:
        return os.path.join(folder_path, odb_files[0])

    folder_name = os.path.basename(folder_path)
    for f in odb_files:
        if os.path.splitext(f)[0] == folder_name:
            return os.path.join(folder_path, f)

    odb_files.sort()
    return os.path.join(folder_path, odb_files[0])

def get_last_step_and_frame(odb):
    if PREFERRED_STEP in odb.steps.keys():
        step = odb.steps[PREFERRED_STEP]
    else:
        step_names = odb.steps.keys()
        step = odb.steps[step_names[-1]]

    frame = step.frames[-1]
    return step.name, frame

def select_main_instance(odb):
    instances = odb.rootAssembly.instances
    inst_names = instances.keys()

    if len(inst_names) == 1:
        return instances[inst_names[0]]

    best_name = None
    best_n = -1

    for name in inst_names:
        n_elem = len(instances[name].elements)
        if n_elem > best_n:
            best_n = n_elem
            best_name = name

    return instances[best_name]

def build_node_coord_map(instance):
    node_coords = {}

    for node in instance.nodes:
        c = node.coordinates
        if len(c) == 2:
            node_coords[node.label] = (c[0], c[1], 0.0)
        else:
            node_coords[node.label] = (c[0], c[1], c[2])

    return node_coords

def compute_element_centroid(element, node_coords):
    xs = []
    ys = []
    zs = []

    for nid in element.connectivity:
        x, y, z = node_coords[nid]
        xs.append(x)
        ys.append(y)
        zs.append(z)

    return (
        sum(xs) / float(len(xs)),
        sum(ys) / float(len(ys)),
        sum(zs) / float(len(zs))
    )

def build_element_centroid_map(instance, node_coords):
    elem_centroids = {}

    for el in instance.elements:
        elem_centroids[el.label] = compute_element_centroid(el, node_coords)

    return elem_centroids

def average_stress_per_element(stress_field):
    tmp = {}

    for v in stress_field.values:
        el = v.elementLabel

        if el not in tmp:
            tmp[el] = {
                'S11_list': [],
                'Mises_list': []
            }

        s11 = v.data[0]
        mises = v.mises

        tmp[el]['S11_list'].append(s11)
        tmp[el]['Mises_list'].append(mises)

    elem_data = {}

    for el in tmp.keys():
        elem_data[el] = {
            'S11': mean(tmp[el]['S11_list']),
            'Mises': mean(tmp[el]['Mises_list'])
        }

    return elem_data

# ============================================================
# ESTRAZIONE
# ============================================================

def extract_summary_and_line(odb_path, output_line_csv):
    odb = openOdb(path=odb_path, readOnly=True)

    try:
        step_name, frame = get_last_step_and_frame(odb)
        print("  Step      : %s" % step_name)
        print("  Frame ID  : %s" % str(frame.incrementNumber))

        if 'S' not in frame.fieldOutputs.keys():
            raise RuntimeError("Campo 'S' non trovato nell'ultimo frame.")

        stress_field = frame.fieldOutputs['S']
        instance = select_main_instance(odb)

        node_coords = build_node_coord_map(instance)
        elem_centroids = build_element_centroid_map(instance, node_coords)
        elem_stress = average_stress_per_element(stress_field)

        rows_all = []

        for el_label in elem_stress.keys():
            if el_label not in elem_centroids:
                continue

            cx, cy, cz = elem_centroids[el_label]
            rows_all.append({
                'elementLabel': el_label,
                'x': cx,
                'y': cy,
                'z': cz,
                'S11': elem_stress[el_label]['S11'],
                'Mises': elem_stress[el_label]['Mises']
            })

        if len(rows_all) == 0:
            raise RuntimeError("Nessun dato stress disponibile dopo ricostruzione.")

        row_max_mises = rows_all[0]
        row_max_s11 = rows_all[0]
        row_min_s11 = rows_all[0]

        for r in rows_all[1:]:
            if r['Mises'] > row_max_mises['Mises']:
                row_max_mises = r
            if r['S11'] > row_max_s11['S11']:
                row_max_s11 = r
            if r['S11'] < row_min_s11['S11']:
                row_min_s11 = r

        summary = {
            'max_mises': row_max_mises['Mises'],
            'max_mises_x': row_max_mises['x'],
            'max_mises_y': row_max_mises['y'],
            'max_s11': row_max_s11['S11'],
            'max_s11_x': row_max_s11['x'],
            'max_s11_y': row_max_s11['y'],
            'min_s11': row_min_s11['S11'],
            'min_s11_x': row_min_s11['x'],
            'min_s11_y': row_min_s11['y']
        }

        line_rows = []

        for r in rows_all:
            if abs(r['y'] - Y_TARGET) <= Y_TOL:
                line_rows.append(r)

        if len(line_rows) == 0:
            raise RuntimeError(
                "Nessun elemento trovato vicino a y=%.3f con tolleranza %.3f. "
                "Aumenta Y_TOL." % (Y_TARGET, Y_TOL)
            )

        line_rows.sort(key=lambda rr: rr['x'])

        f = open(output_line_csv, 'w')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['x', 'y', 'S11', 'Mises'])

        for r in line_rows:
            writer.writerow([
                "%.6f" % r['x'],
                "%.6f" % r['y'],
                "%.6f" % r['S11'],
                "%.6f" % r['Mises']
            ])

        f.close()

        return summary, len(line_rows)

    finally:
        odb.close()

# ============================================================
# MAIN
# ============================================================

def main():
    project_root = find_project_root()

    print("\n=== DEBUG PATH ===")
    print("Working directory: %s" % project_root)

    print("\nContenuto cartella:")
    for item in os.listdir(project_root):
        print(" - %s" % item)

    results_dir = os.path.join(project_root, "results_summary")
    line_dir = os.path.join(results_dir, "line_profiles_phaseC")

    safe_makedirs(results_dir)
    safe_makedirs(line_dir)

    summary_csv = os.path.join(results_dir, "summary_phaseC.csv")

    model_folders = list_model_folders(project_root)

    print("\nModelli trovati:")
    for m in model_folders:
        print(" - %s" % m)

    if len(model_folders) == 0:
        print("\nNessuna cartella modello trovata. Fine.")
        return

    summary_rows = []

    for model_name in model_folders:
        print("\nProcessing model: %s" % model_name)

        folder_path = os.path.join(project_root, model_name)
        odb_path = find_odb_in_folder(folder_path)

        if odb_path is None:
            print("  Nessun ODB trovato nella cartella.")
            continue

        print("  ODB found  : %s" % os.path.basename(odb_path))

        out_line_csv = os.path.join(line_dir, model_name + "_line.csv")

        try:
            summary, n_line = extract_summary_and_line(odb_path, out_line_csv)

            print("  Max Mises  : %.6f" % summary['max_mises'])
            print("  Max S11    : %.6f" % summary['max_s11'])
            print("  Min S11    : %.6f" % summary['min_s11'])
            print("  Line points: %d" % n_line)

            summary_rows.append([
                model_name,
                "%.6f" % summary['max_mises'],
                "%.6f" % summary['max_mises_x'],
                "%.6f" % summary['max_mises_y'],
                "%.6f" % summary['max_s11'],
                "%.6f" % summary['max_s11_x'],
                "%.6f" % summary['max_s11_y'],
                "%.6f" % summary['min_s11'],
                "%.6f" % summary['min_s11_x'],
                "%.6f" % summary['min_s11_y'],
                out_line_csv
            ])

        except Exception as e:
            print("  ERRORE su %s" % model_name)
            print("  %s" % str(e))
            traceback.print_exc()

    fsum = open(summary_csv, 'w')
    writer = csv.writer(fsum, lineterminator='\n')

    writer.writerow([
        'model_name',
        'max_mises', 'max_mises_x', 'max_mises_y',
        'max_s11', 'max_s11_x', 'max_s11_y',
        'min_s11', 'min_s11_x', 'min_s11_y',
        'line_csv_path'
    ])

    for row in summary_rows:
        writer.writerow(row)

    fsum.close()

    print("\nFINE.")
    print("Summary salvato in:")
    print("  %s" % summary_csv)
    print("Profili salvati in:")
    print("  %s" % line_dir)

if __name__ == "__main__":
    main()