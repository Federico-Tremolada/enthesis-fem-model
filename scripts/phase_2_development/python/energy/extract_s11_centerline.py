"""
Script: extract_s11_centerline.py
Author: FEDERICO TREMOLADA

Purpose:
Extract S11 stress distribution along the model centerline.

Models:
- M17
- M18
- Any additional model folder structured in the same way

Input:
- Abaqus .odb files stored inside selected model subfolders

Operations:
- Search target model folders
- Open the corresponding .odb files
- Extract S11 from the last frame of the first step
- Keep only elements close to the centerline
- Save:
    - one CSV for each model
    - one combined CSV
    - one comparison PNG

Output:
- S11_centerline_all_models.csv
- S11_centerline_comparison.png
- individual model CSV files

Notes:
This script is intended for centerline stress comparison.
Update the base_folder and target_folders variables according to your own project structure.
"""

from odbAccess import openOdb
from abaqusConstants import INTEGRATION_POINT
import os
import csv
import traceback

# =========================================================
# USER SETTINGS
# =========================================================

# Base folder containing the target model subfolders.
# Update this path according to your local project structure.
base_folder = os.path.join(os.getcwd(), "models_folder")

# Model subfolders to process.
# Update these names according to your folder structure.
target_folders = [
    "model_1_folder",
    "model_2_folder"
]

y_target = 3.0
y_tol = 0.20

target_instance_name = None

combined_csv = os.path.join(base_folder, "S11_centerline_all_models.csv")
combined_png = os.path.join(base_folder, "S11_centerline_comparison.png")

# =========================================================
# HELPER FUNCTIONS
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
        raise ValueError("Instance '{}' not found in the odb.".format(target_instance_name))

    instance_names = list(asm.instances.keys())
    if len(instance_names) == 0:
        raise ValueError("No instance found in the odb.")

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


def get_s11_from_field_value_data(data):
    """
    Extract S11 robustly from different Abaqus data formats.
    """
    try:
        return float(data[0])
    except:
        pass

    try:
        return float(data.tolist()[0])
    except:
        pass

    try:
        return float(list(data)[0])
    except:
        pass

    raise TypeError("Unrecognized stress field format: {}".format(type(data)))


def extract_s11_by_element(frame, instance):
    """
    Returns:
    elementLabel -> average S11 value over integration points
    """
    if "S" not in frame.fieldOutputs:
        return None

    s_field = frame.fieldOutputs["S"]
    s_sub = s_field.getSubset(region=instance, position=INTEGRATION_POINT)

    elem_vals = {}

    for v in s_sub.values:
        el = v.elementLabel
        data = v.data

        try:
            s11 = get_s11_from_field_value_data(data)
        except:
            print("[WARNING] Unable to read S11 for element {}".format(el))
            continue

        if el not in elem_vals:
            elem_vals[el] = []
        elem_vals[el].append(s11)

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
        writer.writerow(["Model", "ElementLabel", "X_centroid_mm", "Y_centroid_mm", "S11"])
        writer.writerows(rows)


def save_combined_csv(csv_path, rows):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Model", "ElementLabel", "X_centroid_mm", "Y_centroid_mm", "S11"])
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
            s11 = r[4]
            if model not in by_model:
                by_model[model] = []
            by_model[model].append((x, s11))

        plt.figure(figsize=(10, 6))

        for model, pts in sorted(by_model.items()):
            pts_sorted = sorted(pts, key=lambda t: t[0])
            xs = [p[0] for p in pts_sorted]
            ys = [p[1] for p in pts_sorted]
            plt.plot(xs, ys, marker="o", markersize=3, linewidth=1.2, label=model)

        plt.xlabel("Centerline x [mm]")
        plt.ylabel("S11 [MPa]")
        plt.title("Comparison of S11 along the centerline")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_path, dpi=200)
        plt.close()

        print("[OK] Plot saved to: {}".format(png_path))

    except Exception as e:
        print("[WARNING] Unable to create the plot.")
        print("Reason: {}".format(str(e)))


# =========================================================
# MAIN
# =========================================================

def main():
    print("=" * 70)
    print("CENTERLINE S11 EXTRACTION")
    print("=" * 70)
    print("Base folder : {}".format(base_folder))
    print("y_target    : {}".format(y_target))
    print("y_tol       : {}".format(y_tol))
    print("")

    if not os.path.isdir(base_folder):
        print("[ERROR] Base folder does not exist.")
        return

    combined_rows = []

    for folder_name in target_folders:
        folder_path = os.path.join(base_folder, folder_name)

        print("-" * 70)
        print("Source folder: {}".format(folder_name))

        if not os.path.isdir(folder_path):
            print("[WARNING] Folder not found: skipping.")
            continue

        odb_path = find_odb_in_folder(folder_path)

        if odb_path is None:
            print("[WARNING] No ODB found: skipping.")
            continue

        model_name = clean_model_name(folder_name)

        print("Model         : {}".format(model_name))
        print("ODB           : {}".format(os.path.basename(odb_path)))

        odb = None
        try:
            odb = openOdb(path=odb_path, readOnly=True)

            step_name, step, frame = get_first_step_and_last_frame(odb)
            if frame is None:
                print("[WARNING] No frame available.")
                odb.close()
                continue

            print("Step used     : {}".format(step_name))
            print("Frame used    : last")

            instance = choose_instance(odb)
            print("Instance used : {}".format(instance.name))

            node_dict = build_node_dict(instance)
            s11_by_elem = extract_s11_by_element(frame, instance)

            if s11_by_elem is None:
                print("[WARNING] Field output S not found.")
                odb.close()
                continue

            model_rows = []

            for elem in instance.elements:
                elabel = elem.label

                if elabel not in s11_by_elem:
                    continue

                x_c, y_c = element_centroid_2d(elem, node_dict)

                if abs(y_c - y_target) <= y_tol:
                    row = [model_name, elabel, x_c, y_c, s11_by_elem[elabel]]
                    model_rows.append(row)
                    combined_rows.append(row)

            odb.close()

            if len(model_rows) == 0:
                print("[WARNING] No elements found near the centerline.")
                continue

            model_rows = sorted(model_rows, key=lambda r: r[2])

            out_csv = os.path.join(base_folder, model_name + "_S11_centerline.csv")
            save_model_csv(out_csv, model_rows)

            print("[OK] Extracted elements : {}".format(len(model_rows)))
            print("[OK] Model CSV          : {}".format(out_csv))

        except Exception as e:
            print("[ERROR] Problem during extraction.")
            print(str(e))
            traceback.print_exc()
            if odb is not None:
                try:
                    odb.close()
                except:
                    pass

    print("")
    print("=" * 70)
    print("FINAL SAVE")
    print("=" * 70)

    if len(combined_rows) == 0:
        print("[WARNING] No combined data available.")
        return

    combined_rows = sorted(combined_rows, key=lambda r: (r[0], r[2]))
    save_combined_csv(combined_csv, combined_rows)
    print("[OK] Combined CSV saved to: {}".format(combined_csv))

    make_comparison_plot(combined_rows, combined_png)

    print("")
    print("=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
