"""
Script: extract_layers_comparison.py
Author: FEDERICO TREMOLADA

Purpose:
Perform a rapid comparison of power-law n=2 Abaqus models with different
numbers of enthesis layers by extracting global stress metrics and the S11
centerline profile.

Models:
- Any model folder whose name contains L08
- Any model folder whose name contains L12
- Any model folder whose name contains L16
- Additional model folders following the same tag-based naming convention

Input:
- Abaqus .odb files stored inside model subfolders

Operations:
- Automatically search inside the selected base directory for folders containing
  the tags L08, L12, and L16
- Find the corresponding .odb file inside each model folder
- Open the ODB file
- Extract from the last frame of the selected step:
    * max von Mises
    * max S11
    * min S11
- Extract the S11(x) profile along the specimen centerline
- Save one summary CSV
- Save one line-profile CSV inside each model folder
- Save a centralized copy of all line-profile CSV files
- Save an error log CSV if processing errors occur

Output:
- python_results/summary_layers.csv
- <model_name>_line.csv inside each model folder
- python_results/line_profiles/<model_name>_line.csv
- python_results/errors_log.csv

Notes:
This script is intended for rapid comparison of layer-refinement models in
Abaqus Python.
Update the base_folder variable according to your own project structure.
The script uses automatic folder detection based on L08, L12, and L16 tags,
so it does not depend on exact folder names.
"""

from odbAccess import openOdb
import os
import csv
import traceback

# =========================================
# USER SETTINGS
# =========================================

# Base folder containing the model subfolders with .odb files.
# Update this path according to your local project structure.
base_folder = os.path.join(os.getcwd(), "models_folder")

# Tags identifying the models to compare
TARGET_TAGS = ["L08", "L12", "L16"]

# If None, automatically use the first available step
STEP_NAME = None

# Specimen geometry: height = 6 mm -> centerline at y = 3 mm
MID_Y = 3.0
Y_TOL = 0.20

# Output folders
RESULTS_DIR = os.path.join(base_folder, "python_results")
LINE_DIR = os.path.join(RESULTS_DIR, "line_profiles")
SUMMARY_CSV = os.path.join(RESULTS_DIR, "summary_layers.csv")
ERROR_CSV = os.path.join(RESULTS_DIR, "errors_log.csv")

# =========================================
# UTILITY FUNCTIONS
# =========================================

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_matching_folder(root_dir, tag):
    """
    Search in the root folder for the first subfolder containing the given tag.
    Valid examples:
    - PWR_n2_L08
    - M10_PWR_n2_L08_v1
    - test_L08_final
    """
    candidates = []
    for name in os.listdir(root_dir):
        full = os.path.join(root_dir, name)
        if os.path.isdir(full) and tag.lower() in name.lower():
            candidates.append(full)

    if len(candidates) == 0:
        return None

    # Simple sorting for stable behavior
    candidates.sort()
    return candidates[0]

def find_odb_in_folder(folder_path):
    """
    Find the first .odb file inside the folder.
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
            raise RuntimeError("No step found in the ODB.")
        step = odb.steps[step_names[0]]

    if len(step.frames) == 0:
        raise RuntimeError("No frame found in the selected step.")
    frame = step.frames[-1]

    return step, frame

def find_main_instance(odb):
    """
    Return the first available instance.
    """
    instances = odb.rootAssembly.instances
    if not instances:
        raise RuntimeError("No instance found in the assembly.")

    instance_name = list(instances.keys())[0]
    return instances[instance_name]

def get_element_centroids(instance):
    """
    Return:
    dict elementLabel -> (x_centroid, y_centroid)
    """
    centroids = {}

    # Node map for faster access
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
    Extract global summary values and the S11(x) profile along the centerline.
    """
    odb = None
    try:
        odb = openOdb(odb_path, readOnly=True)

        step, frame = get_step_and_last_frame(odb, step_name)
        instance = find_main_instance(odb)
        centroids = get_element_centroids(instance)

        if "S" not in frame.fieldOutputs:
            raise RuntimeError("Field output 'S' not found in the frame.")

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

            # Centerline profile
            if s11 is not None and abs(y_c - MID_Y) <= Y_TOL:
                line_data.append((x_c, s11, elem_label))

        if not mises_vals:
            raise RuntimeError("No von Mises values extracted.")
        if not s11_vals:
            raise RuntimeError("No S11 values extracted.")
        if not line_data:
            raise RuntimeError("No points found on the centerline. Increase Y_TOL.")

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

# =========================================
# MAIN
# =========================================

def main():
    ensure_dir(RESULTS_DIR)
    ensure_dir(LINE_DIR)

    summary_rows = []
    errors = []

    print("=" * 72)
    print("LAYER COMPARISON EXTRACTION - START")
    print("Base folder = {}".format(base_folder))
    print("=" * 72)

    if not os.path.isdir(base_folder):
        print("FATAL ERROR: base_folder does not exist.")
        print(base_folder)
        return

    for tag in TARGET_TAGS:
        print("\n--- Searching model with tag: {} ---".format(tag))

        model_folder = find_matching_folder(base_folder, tag)
        if model_folder is None:
            msg = "No folder found for tag '{}'".format(tag)
            print("ERROR: " + msg)
            errors.append((tag, msg))
            continue

        model_name = os.path.basename(model_folder)
        print("Folder found: {}".format(model_folder))

        odb_path = find_odb_in_folder(model_folder)
        if odb_path is None:
            msg = "No .odb file found in folder '{}'".format(model_name)
            print("ERROR: " + msg)
            errors.append((model_name, msg))
            continue

        print("ODB found: {}".format(os.path.basename(odb_path)))

        try:
            result = extract_summary_and_line(
                odb_path=odb_path,
                model_name=model_name,
                step_name=STEP_NAME
            )

            summary_rows.append(result)

            # Line CSV in the model folder
            model_line_csv = os.path.join(
                model_folder,
                "{}_line.csv".format(model_name)
            )
            write_line_csv(result["line_data"], model_line_csv, model_name)

            # Centralized copy of line profiles
            central_line_csv = os.path.join(
                LINE_DIR,
                "{}_line.csv".format(model_name)
            )
            write_line_csv(result["line_data"], central_line_csv, model_name)

            print("Line profile saved to: {}".format(model_line_csv))
            print("Central line copy saved to: {}".format(central_line_csv))
            print("Step      : {}".format(result["step_name"]))
            print("Frame ID  : {}".format(result["frame_id"]))
            print("Max Mises : {:.6f}".format(result["max_mises"]))
            print("Max S11   : {:.6f}".format(result["max_s11"]))
            print("Min S11   : {:.6f}".format(result["min_s11"]))
            print("Line points: {}".format(len(result["line_data"])))

        except Exception as e:
            msg = "Processing error: {}".format(str(e))
            print("ERROR: " + msg)
            traceback.print_exc()
            errors.append((model_name, msg))

    if summary_rows:
        write_summary_csv(summary_rows, SUMMARY_CSV)
        print("\nSummary saved to: {}".format(SUMMARY_CSV))
    else:
        print("\nNo valid results available for the summary file.")

    if errors:
        write_error_csv(errors, ERROR_CSV)
        print("Error log saved to: {}".format(ERROR_CSV))

    print("\n" + "=" * 72)
    print("EXTRACTION COMPLETED")
    print("=" * 72)

if __name__ == "__main__":
    main()
