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

## Conclusions — Model Comparison and Selection

The comparative analysis of the five interface models highlights the critical role of material transition laws in controlling stress distribution across the tendon–bone interface.

The **sharp interface** exhibits a pronounced stress concentration at the interface, confirming the detrimental effect of abrupt stiffness discontinuities.

The introduction of graded material transitions significantly improves the mechanical response:

* The **linear gradient** reduces peak stress but still presents a relatively abrupt variation in the stress field.
* The **exponential model** provides a smoother redistribution, indicating improved load transfer continuity.
* The **power-law model with n = 0.5** modifies the stress profile but does not significantly mitigate peak stress concentration, as the stiffness increases too rapidly near the tendon region.

In contrast, the **power-law model with n = 2** demonstrates the most favorable behavior:

* it reduces stress concentration more effectively than the other graded models
* it produces a smoother and more continuous stress distribution across the interface
* it delays the stiffness increase, improving mechanical compatibility between tendon and bone

This behavior suggests that a **convex material gradient**, with delayed stiffening, is more effective in mitigating stress concentrations than both linear and concave profiles.

### Model Selection

Based on these results, the **power-law model with exponent n = 2** is selected as the reference configuration for the subsequent phase of the project.

This selection is driven by its superior ability to:

* minimize stress peaks
* ensure gradual load transfer
* reproduce a mechanically consistent transition between soft and stiff tissues

The following phase of the project focuses on further improving this model by introducing additional physical realism, such as variable Poisson’s ratio and energy-based validation.


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
