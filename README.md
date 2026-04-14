# Enthesis FEM Model – Stress Distribution in Functionally Graded Interfaces

## Overview

The tendon-to-bone interface (enthesis) is a complex biological structure characterized by a gradual transition of mechanical properties from soft tendon to stiff bone.

This project investigates how different material distributions affect stress concentration at the interface using Finite Element Modeling (FEM).

The objective is to evaluate whether functionally graded materials (FGMs) reduce stress peaks compared to sharp interfaces and to identify the most effective transition law.

---

## Problem Statement

In many engineered systems, abrupt changes in material properties lead to stress concentrations and potential failure.

In contrast, biological systems often adopt gradual transitions to mitigate these effects.

The enthesis is a prime example of this strategy.

This project aims to:

* model the tendon–bone interface
* introduce different material gradients
* analyze stress distribution along the interface
* identify the most effective material transition law

---

## Model Description

A simplified 2D FEM model is used:

* Tendon region → low stiffness
* Bone region → high stiffness
* Interface (enthesis) → graded material properties

The following configurations are implemented:

* Sharp interface (baseline)
* Linear gradient
* Exponential gradient
* Power-law gradient (n = 0.5)
* Power-law gradient (n = 2)

All models share identical:

* geometry
* mesh
* boundary conditions

Only the material law in the enthesis region is varied, ensuring a controlled comparison.

---

## Methodology

The project follows a structured simulation pipeline:

### Phase A — Model Generation (Abaqus)

* Geometry definition
* Material assignment
* Mesh generation
* Boundary conditions

### Phase B — Post-processing (Python)

* Extraction of:

  * S11 stress
  * stress profiles along the interface
* Export to CSV

### Phase C — Data Analysis (MATLAB / Python)

* Model comparison
* Stress peak evaluation
* Spatial distribution analysis

### Phase D — Model Selection

* Comparative evaluation of all interface laws
* Identification of the model providing:

  * lowest stress concentration
  * smoothest stress transfer
  * physically consistent distribution

---

## Results — Model Comparison

### Global Stress Distribution

![S11 Comparison](results/key_results/S11_comparison_advanced.png)

### Zoom Near the Interface

![S11 Zoom](results/key_results/S11_zoom_all_models.png)

---

## Key Findings

* The **sharp interface** exhibits the highest stress concentration.
* The **linear gradient** reduces peak stress but maintains a relatively abrupt transition.
* The **exponential model** improves stress redistribution.
* The **power-law model (n = 0.5)** alters stress distribution but does not significantly reduce peak values.
* The **power-law model (n = 2)** provides the best balance between peak reduction and smooth load transfer.

---

## Model Selection

Based on the comparative analysis, the **power-law model with exponent n = 2** is selected for further development.

This model shows:

* reduced stress concentration
* smoother stress gradient across the interface
* improved mechanical compatibility between tendon and bone

This marks the transition from **model comparison** to **model refinement** in the next phase of the project.

---

## Repository Structure

```text
docs/      → technical documentation
models/    → FEM model descriptions and screenshots
scripts/   → Python/MATLAB post-processing
results/   → processed data and plots
paper/     → manuscript and figures
```

---

## Notes

This repository focuses on understanding how material gradients influence stress transfer rather than optimizing geometry.

---

## Future Work

* Parametric study of power-law exponents
* Inclusion of nonlinear material behavior
* Energy-based validation
* Comparison with experimental data
