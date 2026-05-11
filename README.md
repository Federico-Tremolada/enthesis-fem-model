# Enthesis FEM Model – Stress and Energy Distribution in Functionally Graded Interfaces

![Python](https://img.shields.io/badge/Python-Abaqus%20Post--Processing-blue)
![MATLAB](https://img.shields.io/badge/MATLAB-Data%20Analysis-orange)
![FEM](https://img.shields.io/badge/Method-Finite%20Element%20Method-green)
![Abaqus](https://img.shields.io/badge/Software-Abaqus-lightgrey)

---

## Overview

The tendon-to-bone interface (enthesis) is a biologically optimized structure characterized by a gradual transition in mechanical properties from compliant tendon to stiff bone.

This project investigates how different material transition laws influence both **stress distribution** and **elastic energy storage** across the interface using Finite Element Modeling (FEM).

The goal is to understand how the **shape of the material gradient controls load transfer mechanisms**, and to identify the most mechanically effective configuration.

---

## Problem Statement

In engineering systems, abrupt changes in material properties generate **stress concentrations** that can lead to structural failure.

Biological interfaces, such as the enthesis, overcome this issue through **functionally graded transitions**, enabling smooth load transfer between dissimilar materials.

This project aims to:

- model the tendon–bone interface using FEM  
- implement different material gradient laws  
- analyze stress distribution (S11)  
- evaluate elastic energy distribution (SENER)  
- identify the most effective transition strategy  

---

## Model Description

A simplified 2D FEM model is used to isolate the effect of material grading.

- Tendon → compliant material (E = 200 MPa)  
- Bone → stiff material (E = 20000 MPa)  
- Enthesis → graded transition region  

All simulations share:

- identical geometry (30 mm × 6 mm)  
- identical boundary conditions (imposed displacement)  
- identical mesh strategy  

Only the **material law in the enthesis region** is varied, ensuring a controlled comparison.

---

## Methodology

The project follows a structured and fully reproducible pipeline:

### 1. FEM Simulation (Abaqus)

- geometry and partitioning  
- material assignment  
- mesh generation  
- boundary conditions  
- solution stored as `.odb`  

---

### 2. Data Extraction (Python)

Extraction of physically meaningful quantities:

- S11 stress component  
- stress profiles along the interface  
- elastic strain energy (SENER)  

Outputs:

- structured CSV datasets  
- model-wise and combined results  

---

### 3. Data Analysis (MATLAB / Python)

- interpolation on a common spatial grid  
- comparison of S11(x) distributions  
- energy distribution analysis  
- stress–energy correlation  
- computation of quantitative metrics  
- generation of publication-ready figures  

---

## Phase 1 — Baseline Model Comparison

### Implemented Configurations

- Sharp interface (discontinuous)  
- Linear gradient  
- Exponential gradient  
- Power-law (n = 0.5)  
- Power-law (n = 2)  

### Key Findings

- Sharp interface → highest stress concentration  
- Linear / exponential → partial stress smoothing  
- Power-law → most effective redistribution  

> Among Phase 1 models, **power-law (n = 2)** provides the best balance between:

- peak reduction  
- distribution symmetry  
- mechanical consistency  

---

## Transition to Phase 2 — Model Optimization

Before introducing additional physical effects, the model was refined through a parametric study:

### Discretization Refinement

- enthesis discretized into increasing number of layers  
- convergence achieved at **16 layers**  
- ensures smooth and mesh-independent stress profiles  

### Power-Law Sensitivity

Exponent tested:

- n = 1.5  
- n = 2  
- n = 3  
- n = 5  

### Key Result

The configuration:

- **power-law with n = 3**  
- **16 layers**

provides the best trade-off between:

- stress peak reduction  
- spatial regularity  
- physically consistent load transfer  

> This becomes the **reference model** for all subsequent analyses.

---

## Phase 2 — Advanced Model Development

### Objectives

- increase physical realism  
- validate stress-based results  
- test robustness of the optimal configuration  

---

### Variable Poisson’s Ratio

- spatial variation of ν across the enthesis  
- comparison with constant ν model  

### Results

- negligible influence on global response  
- slight redistribution of local stress  
- no improvement in peak reduction  

> The mechanical behavior is dominated by **stiffness gradient E(x)**

---

### Elastic Energy Analysis

- extraction of SENER  
- spatial distribution along the interface  
- comparison between models  

### Key Results

- total elastic energy ≈ identical between models  
- energy localization matches stress gradients  
- strong correlation between S11 and SENER  

Confirms that:

- stress redistribution is supported by energy redistribution  
- graded interfaces improve mechanical compatibility  

---

## Key Engineering Insight

The study demonstrates that:

> **The shape of the stiffness gradient directly controls stress transfer mechanisms**

The optimal configuration:

- **power-law (n = 3, 16 layers)**  

provides:

- reduced stress concentration  
- smooth load transfer  
- distributed elastic energy  

---

## Why This Matters

Understanding graded interfaces is critical for:

- tendon-to-bone repair strategies  
- biomimetic material design  
- interface engineering in multi-material systems  

---

## Visual Results

### Stress Distribution

![S11 comparison](docs/images/S11_comparison_advanced.png)

---

### Elastic Energy Distribution

![Energy distribution](docs/images/SENER_comparison.png)

---

## Final Conclusions

- Sharp interfaces produce non-physiological stress concentrations  
- Graded materials significantly improve mechanical behavior  
- The **form of the gradient** is more important than its mere presence  
- The **power-law model (n = 3)** is the most effective configuration  
- Poisson’s ratio variation has a secondary role  
- Elastic energy analysis confirms the physical consistency of the model  

---

## Reproducibility

The entire workflow is fully reproducible:

1. run Abaqus simulations  
2. execute Python extraction scripts  
3. run MATLAB/Python analysis  

All intermediate data is stored in CSV format.

---

## Repository Structure

```text
docs/      → technical documentation  
models/    → FEM model descriptions  
scripts/   → Python/MATLAB post-processing  
results/   → processed data and plots  
paper/     → manuscript and figures

```

---

## Final Remark

This project provides a structured framework to study stress transfer in graded interfaces, bridging biomechanical insight and engineering design.

It establishes a solid foundation for future developments:

- Nonlinear materials
- Anisotropy
- 3D modeling
- Biomimetic implant design

---

# Author

**Federico Tremolada**  
Biomedical Engineer — Politecnico di Milano  
