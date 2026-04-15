# Scripts

This folder contains all post-processing and analysis scripts used to extract, process, and interpret results from the FEM simulations of the tendon–bone interface.

The scripting pipeline is designed to be:

- reproducible  
- modular  
- physically interpretable  
- directly aligned with the research workflow  

---

## Workflow Overview

The complete pipeline follows three main stages:

### 1. Abaqus (Simulation)

- FEM models are built and solved in Abaqus  
- Material gradients (power-law, linear, etc.) are implemented  
- Results are stored in `.odb` files  

---

### 2. Python (Data Extraction)

Python scripts interface directly with Abaqus `.odb` files to extract physically meaningful quantities.

**Main extracted data:**

- Stress components (S11)  
- Elastic strain energy (SENER / ALLSE)  
- Spatial distributions along the interface  

**Outputs:**

- Structured CSV files  
- Clean datasets for downstream analysis  

---

### 3. MATLAB / Python (Data Analysis)

Extracted data is analyzed to:

- compare different material models  
- evaluate stress redistribution along the interface  
- study energy–stress relationships  
- compute quantitative metrics  
- generate publication-ready plots  

---

## Python Scripts

Python scripts are responsible for data extraction from Abaqus and part of the analysis.

### Extraction Scripts

#### `extract_summary.py`

Extracts global mechanical metrics from `.odb` files.

**Outputs:**

- Maximum von Mises stress  
- Maximum and minimum S11  
- Summary CSV file across models  

---

#### `extract_line.py`

Extracts stress values along a predefined line (interface / centerline).

**Outputs:**

- CSV file containing:
  - spatial coordinate (x)  
  - S11 stress  

---

#### `extract_s11_centerline.py`

Extracts S11 specifically along the model centerline.

**Features:**

- element-based extraction  
- centroid filtering (geometric selection)  
- multi-model comparison  

**Outputs:**

- per-model CSV  
- combined CSV  
- comparison plot  

---

#### `extract_sener_centerline.py`

Extracts elastic strain energy density (SENER) along the centerline.

**Purpose:**

- quantify energy distribution across the interface  
- support physical interpretation of stress smoothing  

---

### Analysis Scripts

#### `analyze_S11_all.py`

Performs comparative analysis of stress distributions.

**Functions:**

- alignment of spatial coordinates  
- multi-model comparison  
- generation of plots  

---

#### `analyze_sener_centerline.py`

Analyzes spatial distribution of elastic energy.

**Functions:**

- comparison between models  
- identification of energy concentration zones  
- support for stress–energy correlation  

---

#### `final_s11_vs_sener.py`

Core script for advanced interpretation.

**Functions:**

- correlates S11 and SENER  
- evaluates local vs global mechanical response  
- provides key data for the Discussion section  

---

## MATLAB Scripts

MATLAB is used for structured numerical analysis and visualization.

---

### `compare_phaseB_results.m`

Baseline comparison of different gradient models.

**Functions:**

- interpolation on a common spatial grid  
- stress comparison plots  
- evaluation of peak reduction  

---

### `compare_phaseC_results.m`

Analysis of physically enhanced models (variable Poisson ratio).

**Functions:**

- comparison between constant and variable ν  
- evaluation of transverse contraction effects  
- quantitative comparison metrics  

---

## Data Flow
Abaqus (.odb) --> Python extraction --> CSV datasets --> MATLAB / Python analysis --> Plots + metrics (results/)

---

## Key Assumptions

To ensure consistency across simulations:

- identical geometry across all models  
- consistent reference coordinate system  
- identical extraction line definition  
- comparable mesh density in the interface region  

---

## Engineering Purpose

This scripting pipeline enables:

- rigorous comparison between sharp and graded interfaces  
- quantitative evaluation of stress redistribution  
- analysis of elastic energy as a validation metric  
- reproducible and scalable post-processing  

It constitutes the **analytical backbone** of the project and directly supports:

- result interpretation  
- validation against literature  
- scientific paper development  
