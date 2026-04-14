# Scripts

This folder contains the post-processing and analysis scripts used to extract and evaluate results from the FEM simulations of the tendon–bone interface.

The workflow is structured to ensure reproducibility and a clear separation between data extraction and analysis.

---

## Workflow Overview

The complete pipeline follows three main stages:

### 1. Abaqus (Simulation)

* FEM models are built and solved in Abaqus
* Results are stored in `.odb` files

### 2. Python (Data Extraction)

Python scripts are used to extract numerical data from Abaqus results:

* extraction of global stress metrics
* extraction of stress profiles along the interface
* export of data into CSV format

### 3. MATLAB / Python (Data Analysis)

Extracted data is processed to:

* compare different material models
* evaluate stress distributions
* compute quantitative metrics
* generate figures for interpretation

---

## Folder Structure

### Python Scripts

- `extract_summary.py` → extracts global stress metrics from Abaqus results
- `extract_line_S11.py` → extracts S11 along the interface
- `analyze_S11_all.py` → compares all models and generates final plots

### MATLAB Scripts

- `plot_S11_comparison.m` → visual comparison of stress distributions
- `advanced_analysis.m` → gradient and curvature analysis
- `metrics_analysis.m` → quantitative comparison between models

---

## Python Scripts

### `extract_summary.py`

Extracts global stress metrics from Abaqus `.odb` files.

**Outputs:**

* maximum von Mises stress
* maximum and minimum S11
* summary CSV file

---

### `extract_line.py`

Extracts the stress profile along a predefined line at the interface.

**Outputs:**

* CSV file containing:

  * x coordinate
  * S11 stress

---

### `analyze_S11_all.py`

Performs comparative analysis across all models.

**Functions:**

* reads CSV data
* aligns spatial coordinates
* generates comparative plots

---

## MATLAB Scripts

### `postprocess_enthesis.m`

Performs baseline analysis of S11 distributions.

**Functions:**

* interpolation on a common grid
* comparison plots
* basic stress metrics

---

### `postprocess_enthesis_advanced.m`

Performs advanced mechanical analysis.

**Functions:**

* gradient (dS/dx) computation
* curvature (d²S/dx²) analysis
* advanced metrics
* model ranking

---

## Data Flow

```text
Abaqus (.odb)
     ↓
Python extraction
     ↓
CSV files
     ↓
MATLAB / Python analysis
     ↓
Plots + metrics (results/)
```

---

## Notes

* All models must use the same geometry and reference system to ensure consistency
* The extraction line must be identical across simulations
* CSV files generated here are stored and used in the `results/` folder

---

## Purpose

This scripting pipeline enables:

* reproducible analysis
* consistent comparison between models
* quantitative evaluation of stress distributions

It represents the core analytical backbone of the project.
