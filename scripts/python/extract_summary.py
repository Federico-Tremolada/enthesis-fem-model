# -*- coding: utf-8 -*-
"""
extract_summary.py

Post-processing Abaqus ODB files to extract summary stress metrics
from the last frame of the loading step.

Extracted quantities:
- max von Mises stress
- max S11
- min S11
- number of stress values read

Designed to run with Abaqus Python:
    abaqus python extract_summary.py

Assumed folder structure:
root_folder/
│
├── M01_sharp_v1/
│   └── M01_sharp_v1.odb
├── M02_linear_v1/
│   └── M02_linear_v1.odb
└── ...

Output:
- summary_all_models.csv
"""

import os
import csv
from odbAccess import openOdb
from abaqusConstants import INTEGRATION_POINT


def find_model_folders(root_dir):
    """
    Return subfolders that may contain model ODB files.
    Ignores hidden folders and common non-model folders.
    """
    ignore_names = {
        'python',
        'matlab',
        'figures',
        '__pycache__'
    }

    model_dirs = []
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)

        if not os.path.isdir(full_path):
            continue
        if name.startswith('.'):
            continue
        if name in ignore_names:
            continue

        model_dirs.append(full_path)

    model_dirs.sort()
    return model_dirs


def find_odb_in_folder(folder_path):
    """
    Find the ODB file inside a model folder.

    Priority:
    1) file matching folder name
    2) first .odb found
    """
    folder_name = os.path.basename(folder_path)
    expected_odb = os.path.join(folder_path, folder_name + '.odb')

    if os.path.isfile(expected_odb):
        return expected_odb

    odb_files = []
    for name in os.listdir(folder_path):
        if name.lower().endswith('.odb'):
            odb_files.append(os.path.join(folder_path, name))

    odb_files.sort()

    if len(odb_files) == 0:
        return None

    return odb_files[0]


def choose_step(odb):
    """
    Select the most appropriate analysis step.

    Priority:
    1) step named 'Loading'
    2) last step different from 'Initial'
    3) if only one exists, use that
    """
    step_names = list(odb.steps.keys())

    if 'Loading' in step_names:
        return 'Loading'

    non_initial_steps = [name for name in step_names if name != 'Initial']
    if len(non_initial_steps) > 0:
        return non_initial_steps[-1]

    if len(step_names) > 0:
        return step_names[-1]

    return None


def extract_summary_from_odb(odb_path):
    """
    Open an ODB and extract summary metrics from stress field S
    at the last frame of the selected step.

    Returns a dictionary ready to be written to CSV.
    """
    odb = None

    result = {
        'model_name': os.path.splitext(os.path.basename(odb_path))[0],
        'odb_path': odb_path,
        'step_name': '',
        'frame_id': '',
        'frame_value': '',
        'max_mises': '',
        'max_s11': '',
        'min_s11': '',
        'n_values': '',
        'status': 'OK',
        'message': ''
    }

    try:
        odb = openOdb(path=odb_path, readOnly=True)

        step_name = choose_step(odb)
        if step_name is None:
            raise Exception('No valid step found in ODB.')

        step = odb.steps[step_name]

        if len(step.frames) == 0:
            raise Exception('Selected step has no frames.')

        frame = step.frames[-1]

        result['step_name'] = step_name
        result['frame_id'] = len(step.frames) - 1
        result['frame_value'] = frame.frameValue

        if 'S' not in frame.fieldOutputs.keys():
            raise Exception("Field output 'S' not found in selected frame.")

        stress_field = frame.fieldOutputs['S']

        # Restrict explicitly to integration points when available
        try:
            stress_field = stress_field.getSubset(position=INTEGRATION_POINT)
        except Exception:
            pass

        values = stress_field.values

        if len(values) == 0:
            raise Exception("No stress values found in field output 'S'.")

        max_mises = None
        max_s11 = None
        min_s11 = None

        for v in values:
            mises = v.mises
            s11 = v.data[0]

            if (max_mises is None) or (mises > max_mises):
                max_mises = mises

            if (max_s11 is None) or (s11 > max_s11):
                max_s11 = s11

            if (min_s11 is None) or (s11 < min_s11):
                min_s11 = s11

        result['max_mises'] = max_mises
        result['max_s11'] = max_s11
        result['min_s11'] = min_s11
        result['n_values'] = len(values)

    except Exception as e:
        result['status'] = 'ERROR'
        result['message'] = str(e)

    finally:
        if odb is not None:
            odb.close()

    return result


def write_csv(output_csv, rows):
    """
    Write summary results to CSV.
    Compatible with Abaqus Python 3.x.
    """
    fieldnames = [
        'model_name',
        'odb_path',
        'step_name',
        'frame_id',
        'frame_value',
        'max_mises',
        'max_s11',
        'min_s11',
        'n_values',
        'status',
        'message'
    ]

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    """
    Main workflow:
    - use current working directory as project root
    - search model folders
    - find ODB in each folder
    - extract summary metrics
    - save CSV
    """
    root_dir = os.getcwd()
    print('Root directory: {}'.format(root_dir))

    model_dirs = find_model_folders(root_dir)

    if len(model_dirs) == 0:
        print('No model folders found.')
        return

    all_results = []

    for model_dir in model_dirs:
        folder_name = os.path.basename(model_dir)
        print('\nProcessing folder: {}'.format(folder_name))

        odb_path = find_odb_in_folder(model_dir)

        if odb_path is None:
            print('  No ODB found.')
            all_results.append({
                'model_name': folder_name,
                'odb_path': '',
                'step_name': '',
                'frame_id': '',
                'frame_value': '',
                'max_mises': '',
                'max_s11': '',
                'min_s11': '',
                'n_values': '',
                'status': 'ERROR',
                'message': 'No ODB file found in folder.'
            })
            continue

        print('  ODB found: {}'.format(os.path.basename(odb_path)))

        result = extract_summary_from_odb(odb_path)
        all_results.append(result)

        if result['status'] == 'OK':
            print('  Step       : {}'.format(result['step_name']))
            print('  Frame ID   : {}'.format(result['frame_id']))
            print('  Frame value: {}'.format(result['frame_value']))
            print('  Max Mises  : {}'.format(result['max_mises']))
            print('  Max S11    : {}'.format(result['max_s11']))
            print('  Min S11    : {}'.format(result['min_s11']))
            print('  N values   : {}'.format(result['n_values']))
        else:
            print('  ERROR      : {}'.format(result['message']))

    output_csv = os.path.join(root_dir, 'summary_all_models.csv')
    write_csv(output_csv, all_results)

    print('\nDone.')
    print('Summary written to: {}'.format(output_csv))


if __name__ == '__main__':
    main()