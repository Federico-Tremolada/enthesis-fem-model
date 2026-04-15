"""
Script: extract_energy_allse.py
Author: FEDERICO TREMOLADA

Purpose:
Extract total elastic strain energy (ALLSE) from Abaqus models.

Models:
- M17
- M18
- Any additional model folder structured in the same way

Input:
- Abaqus .odb files stored inside model subfolders

Operations:
- Search all subfolders inside the selected base directory
- Find the corresponding .odb file
- Extract final ALLSE value from history output
- Save a summary CSV
- Optionally generate a bar chart PNG

Output:
- energy_summary.csv
- energy_summary.png

Notes:
This script is intended for global energy comparison between models.
Update the base_folder variable according to your own project structure.
"""

from odbAccess import openOdb
import os
import csv
import traceback

# =========================================
# USER SETTINGS
# =========================================

# Base folder containing model subfolders with .odb files.
# Update this path according to your local project structure.
base_folder = os.path.join(os.getcwd(), "models_folder")

output_csv = os.path.join(base_folder, "energy_summary.csv")
output_png = os.path.join(base_folder, "energy_summary.png")

# If True, search ONLY for the .odb file with the same name as the folder
strict_same_name = True

# =========================================
# FUNCTIONS
# =========================================

def find_matching_odb(folder_path, folder_name):
    """
    Search for the .odb file inside the folder.
    If strict_same_name=True, search for folder_name.odb
    Otherwise, return the first available .odb file.
    """
    expected_odb = os.path.join(folder_path, folder_name + ".odb")

    if strict_same_name:
        if os.path.isfile(expected_odb):
            return expected_odb
        return None

    # fallback: first .odb found
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".odb"):
            return os.path.join(folder_path, fname)

    return None


def extract_final_allse(odb_path):
    """
    Extract the final ALLSE value from the first available step.
    Search for ALLSE in history regions.
    Return:
        final_allse, step_name, history_region_key
    If ALLSE is not found, return:
        None, step_name, None
    """
    odb = None
    try:
        odb = openOdb(path=odb_path, readOnly=True)

        if not odb.steps:
            return None, None, None

        # First available step
        step_name = list(odb.steps.keys())[0]
        step = odb.steps[step_name]

        # Search ALLSE in all history regions
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
    Optional plot:
    save a PNG bar chart with final ALLSE values for valid models.
    If matplotlib is not available in the Abaqus environment, skip without error.
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
        print("[INFO] No valid data available to generate the chart.")
        return

    try:
        import matplotlib
        matplotlib.use("Agg")  # save without opening windows
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        plt.bar(valid_models, valid_values)
        plt.ylabel("Final ALLSE")
        plt.title("Comparison of total elastic strain energy (ALLSE)")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(png_path, dpi=200)
        plt.close()

        print("[OK] Plot saved to: {}".format(png_path))

    except Exception as e:
        print("[WARNING] Unable to create PNG chart.")
        print("Reason: {}".format(str(e)))


# =========================================
# MAIN
# =========================================

def main():
    print("=" * 60)
    print("AUTOMATIC ALLSE EXTRACTION FROM ODB FILES")
    print("=" * 60)
    print("Base folder : {}".format(base_folder))
    print("CSV output  : {}".format(output_csv))
    print("PNG output  : {}".format(output_png))
    print("")

    if not os.path.isdir(base_folder):
        print("[ERROR] Base folder does not exist.")
        return

    results = []

    subfolders = [
        name for name in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, name))
    ]

    if len(subfolders) == 0:
        print("[ERROR] No subfolders found inside the base folder.")
        return

    for folder_name in sorted(subfolders):
        folder_path = os.path.join(base_folder, folder_name)
        print("-" * 60)
        print("Model: {}".format(folder_name))

        odb_path = find_matching_odb(folder_path, folder_name)

        if odb_path is None:
            print("[WARNING] No .odb file found with the same name as the folder.")
            results.append([
                folder_name,
                "",
                "",
                "",
                None,
                "ODB_NOT_FOUND"
            ])
            continue

        print("ODB found: {}".format(os.path.basename(odb_path)))

        try:
            final_allse, step_name, region_key = extract_final_allse(odb_path)

            if final_allse is None:
                print("[WARNING] ALLSE not found in history outputs.")
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
                print("[OK] Final ALLSE  : {}".format(final_allse))

                results.append([
                    folder_name,
                    os.path.basename(odb_path),
                    step_name,
                    region_key,
                    final_allse,
                    "OK"
                ])

        except Exception as e:
            print("[ERROR] Failed to read ODB file.")
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
    print("SAVING RESULTS")
    print("=" * 60)

    save_csv(results, output_csv)
    print("[OK] CSV saved to: {}".format(output_csv))

    make_bar_chart(results, output_png)

    print("")
    print("=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
