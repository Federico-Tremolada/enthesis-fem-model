# Post-Processing Pipeline

This document describes the workflow used to extract, process, and analyze the results obtained from FEM simulations.

The pipeline is designed to ensure consistency, reproducibility, and quantitative comparison between different models of the tendon–bone interface.

---

## 1. Overview

The post-processing workflow is divided into three main stages:

1. Abaqus → simulation results (.odb)
2. Python → data extraction
3. MATLAB / Python → data analysis and visualization

---

## 2. Abaqus Output

Each simulation produces an `.odb` file containing:

* stress fields
* deformation fields
* element and node data

### Relevant quantities

* **S11** → longitudinal stress (primary variable)
* **von Mises stress** → global stress indicator (secondary)

---

## 3. Python — Data Extraction

Python is used to extract numerical data from `.odb` files.

### 3.1 Line Extraction

Script: `extract_line.py`

**Purpose:**

* Extract S11 along a predefined line crossing the enthesis

**Output:**

CSV file with:

* x → coordinate along the interface [mm]
* S11 → stress value [MPa]

---

### 3.2 Global Metrics Extraction

Script: `extract_summary.py`

**Purpose:**

* Extract global stress indicators

**Output:**

CSV file containing:

* maximum von Mises stress
* maximum S11
* minimum S11

---

## 4. Data Organization

All extracted data is stored as CSV files.

### Structure

* One CSV per model for line data
* One summary CSV for global metrics

This ensures:

* easy portability
* compatibility with multiple tools
* reproducibility

---

## 5. MATLAB / Python — Data Analysis

### 5.1 Baseline Analysis

Script: `postprocess_enthesis.m`

**Operations:**

* interpolation on a common spatial grid
* comparison of S11(x) profiles
* extraction of key metrics:

  * max/min S11
  * S11 at interface
  * peak locations

---

### 5.2 Advanced Analysis

Script: `postprocess_enthesis_advanced.m`

**Additional operations:**

* computation of stress gradient:

  * dS/dx
* computation of stress curvature:

  * d²S/dx²
* smoothness evaluation
* comparison with sharp model
* model ranking

---

### 5.3 Python Visualization (optional)

Script: `analyze_S11_all.py`

**Purpose:**

* quick comparison plots
* validation of extracted data
* cross-check with MATLAB results

---

## 6. Key Metrics

The following quantities are used to compare models:

### Local behavior

* S11 at the interface
* maximum stress values
* position of stress peaks

### Gradient-based metrics

* max |dS/dx| → severity of stress variation
* mean |d²S/dx²| → stress concentration indicator

### Global behavior

* area under S11 curve
* difference with respect to sharp model

---

## 7. Interpretation Strategy

The analysis is based on the following principles:

* smoother stress transitions are preferable
* lower stress gradients indicate better load transfer
* reduced curvature implies lower stress concentration

The goal is to identify the material law that provides the most mechanically efficient transition.

---

## 8. Output of the Pipeline

The pipeline produces:

* comparative plots of S11(x)
* gradient and curvature plots
* summary tables of metrics
* ranking of models

All outputs are stored in the `results/` folder.

---

## 9. Reproducibility

The workflow is fully reproducible:

1. run Abaqus simulations
2. execute Python extraction scripts
3. run MATLAB analysis scripts

No manual intervention is required beyond selecting input folders.

---

## Summary

The post-processing pipeline transforms raw FEM data into:

* interpretable stress distributions
* quantitative performance metrics
* objective comparison between models

This enables a rigorous evaluation of material gradient strategies in the tendon–bone interface.
