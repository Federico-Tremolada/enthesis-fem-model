# -*- coding: utf-8 -*-

import os
import csv
from odbAccess import openOdb
from abaqusConstants import INTEGRATION_POINT


def find_model_folders(root_dir):
    ignore = {
        'python',
        'matlab',
        '__pycache__',
        '.git'
    }

    folders = []
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)

        if not os.path.isdir(path):
            continue
        if name.startswith('.'):
            continue
        if name in ignore:
            continue

        folders.append(path)

    folders.sort()
    return folders


def find_odb(folder):
    folder_name = os.path.basename(folder)
    expected = os.path.join(folder, folder_name + '.odb')

    if os.path.isfile(expected):
        return expected

    odbs = []
    for f in os.listdir(folder):
        if f.lower().endswith('.odb'):
            odbs.append(os.path.join(folder, f))

    odbs.sort()

    if len(odbs) == 0:
        return None

    return odbs[0]


def choose_step(odb):
    names = list(odb.steps.keys())

    if 'Loading' in names:
        return 'Loading'

    non_initial = [n for n in names if n != 'Initial']
    if len(non_initial) > 0:
        return non_initial[-1]

    return names[-1]


def get_single_instance(odb):
    instances = odb.rootAssembly.instances
    instance_names = list(instances.keys())

    if len(instance_names) == 0:
        raise Exception('No instances found in rootAssembly.')

    if len(instance_names) > 1:
        print("  WARNING: multiple instances found. Using first instance: {}".format(instance_names[0]))

    return instances[instance_names[0]]


def build_node_coord_map(instance):
    node_map = {}

    for node in instance.nodes:
        node_map[node.label] = (node.coordinates[0], node.coordinates[1])

    return node_map


def compute_element_centroid(element, node_coord_map):
    xs = []
    ys = []

    for node_label in element.connectivity:
        x, y = node_coord_map[node_label]
        xs.append(x)
        ys.append(y)

    xc = sum(xs) / float(len(xs))
    yc = sum(ys) / float(len(ys))

    return xc, yc


def build_element_centroid_map(instance):
    node_coord_map = build_node_coord_map(instance)
    elem_map = {}

    for elem in instance.elements:
        elem_map[elem.label] = compute_element_centroid(elem, node_coord_map)

    return elem_map


def extract_line(odb_path):
    odb = openOdb(odb_path, readOnly=True)

    model_name = os.path.splitext(os.path.basename(odb_path))[0]
    step_name = choose_step(odb)
    step = odb.steps[step_name]
    frame = step.frames[-1]

    if 'S' not in frame.fieldOutputs.keys():
        odb.close()
        raise Exception("Field output 'S' not found.")

    stress = frame.fieldOutputs['S']

    try:
        stress = stress.getSubset(position=INTEGRATION_POINT)
    except Exception:
        pass

    instance = get_single_instance(odb)
    elem_centroids = build_element_centroid_map(instance)

    all_y = [coord[1] for coord in elem_centroids.values()]
    min_y = min(all_y)
    max_y = max(all_y)
    y_center = 0.5 * (min_y + max_y)

    print("  Y range         : min = {:.3f}, max = {:.3f}".format(min_y, max_y))
    print("  Computed center : y = {:.3f}".format(y_center))

    distances = []

    for elem_label, (x, y) in elem_centroids.items():
        d = abs(y - y_center)
        distances.append(d)

    min_dist = min(distances)

    print("  Min distance from center: {:.4f}".format(min_dist))

    tol_row = 1e-6
    data = []

    for s_val in stress.values:
        elem_label = s_val.elementLabel

        if elem_label not in elem_centroids:
            continue

        x, y = elem_centroids[elem_label]
        d = abs(y - y_center)

        if abs(d - min_dist) < tol_row:
            s11 = s_val.data[0]
            mises = s_val.mises

            if abs(x) < 1e6:
                data.append([x, s11, mises, model_name, step_name])

    odb.close()

    data.sort(key=lambda row: row[0])

    return data


def save_csv(output_path, data):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'S11', 'Mises', 'model_name', 'step_name'])
        writer.writerows(data)


def main():
    root = os.getcwd()
    folders = find_model_folders(root)

    if len(folders) == 0:
        print("No model folders found.")
        return

    for folder in folders:
        name = os.path.basename(folder)
        print("\nProcessing: {}".format(name))

        odb_path = find_odb(folder)

        if odb_path is None:
            print("  No ODB found")
            continue

        print("  ODB: {}".format(os.path.basename(odb_path)))

        try:
            data = extract_line(odb_path)

            print("  Points extracted: {}".format(len(data)))

            out_csv = os.path.join(folder, "{}_line.csv".format(name))
            save_csv(out_csv, data)

            print("  Saved: {}".format(out_csv))

        except Exception as e:
            print("  ERROR: {}".format(str(e)))


if __name__ == "__main__":
    main()