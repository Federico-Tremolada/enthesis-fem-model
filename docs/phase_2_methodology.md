# Phase 2 — Model Refinement and Physical Validation

## Objective

The second phase of the project aims to enhance the physical reliability of the selected model by:

* improving spatial resolution of the graded interface
* analyzing sensitivity to the material law exponent
* introducing additional physical realism
* validating results using energy-based metrics
* comparing trends with functionally graded material (FGM) theory

This phase builds upon the results of Phase 1, where the power-law model (n = 2) was identified as the most effective configuration.

---

## Overview of Sub-Phases

Phase 2 is structured into five sequential steps:

1. Mesh refinement of the enthesis region
2. Sensitivity analysis on the power-law exponent
3. Introduction of variable Poisson’s ratio
4. Elastic energy analysis
5. Scientific validation against FGM theory

Each step isolates a specific aspect of the model to ensure controlled and interpretable results.

---

## 1. Interface Refinement

### Objective

Evaluate the influence of spatial discretization of the enthesis on stress distribution.

### Models

* M10 → 8 layers (baseline)
* M11 → 12 layers
* M12 → 16 layers

All models use:

* power-law material distribution
* exponent n = 2

### Analysis

* comparison of S11(x) profiles
* evaluation of stress peaks
* assessment of smoothness

### Outcome

The model with **16 layers** is selected for subsequent analysis, as it provides:

* improved resolution of the material gradient
* smoother stress distribution
* negligible increase in computational cost

---

## 2. Sensitivity to Power-Law Exponent

### Objective

Determine how the exponent of the power-law affects stress transfer.

### Models

* M13 → n = 1.5
* M14 → n = 2
* M15 → n = 3
* M16 → n = 5

All models use:

* 16 enthesis layers
* identical geometry and boundary conditions

### Analysis

* comparison of S11(x) distributions
* evaluation of peak stress values
* analysis of stress gradients

### Outcome

The model with **n = 3** is selected as the optimal configuration, as it provides:

* reduced stress concentration
* smoother transition compared to n = 2
* improved load transfer behavior

---

## 3. Effect of Poisson’s Ratio

### Objective

Investigate the influence of transverse deformation on stress distribution.

### Models

* M17 → constant Poisson’s ratio
* M18 → spatially varying Poisson’s ratio

Both models use:

* 16 layers
* power-law exponent n = 3

### Implementation

* Poisson’s ratio varies from tendon to bone
* consistent with the material gradient

### Analysis

* comparison of S11(x)
* evaluation of peak stress values
* qualitative assessment of differences

### Outcome

The variation of Poisson’s ratio shows **limited influence** on the stress distribution.

This suggests that:

* the longitudinal stiffness gradient is the dominant factor
* transverse effects play a secondary role in this configuration

---

## 4. Elastic Energy Analysis

### Objective

Validate the mechanical behavior using an energy-based approach.

### Method

* extraction of strain energy density (SENER) from Abaqus
* analysis along the same interface line used for S11

### Models

* M17 (constant ν)
* M18 (variable ν)

### Analysis

* comparison of energy distribution
* identification of energy concentration zones
* evaluation of smoothness

### Interpretation

A physically consistent model should:

* avoid localized energy peaks
* distribute energy gradually across the interface

This analysis provides an additional validation layer beyond stress-based metrics.

---

## 5. Scientific Validation

### Objective

Compare numerical results with established trends in functionally graded materials (FGMs).

### Approach

* qualitative comparison with literature
* verification of expected behavior:

  * reduced stress concentration
  * smoother stress transfer
  * improved mechanical compatibility

### Outcome

The results are consistent with FGM theory, confirming that:

* graded material transitions reduce stress concentration
* convex stiffness profiles (e.g., power-law with n > 1) improve load transfer

---

## Final Outcome of Phase 2

The optimal model configuration is defined as:

* **16 layers in the enthesis region**
* **power-law material distribution with n = 3**
* **constant Poisson’s ratio (sufficient approximation)**

### Key Achievements

* improved spatial resolution
* optimized material gradient
* validated mechanical behavior
* confirmed consistency with FGM theory

---

## Role in the Overall Project

Phase 2 transforms the initial model into a **physically validated configuration**, providing:

* stronger scientific credibility
* deeper mechanical interpretation
* a solid basis for publication

This phase represents the transition from exploratory modeling to validated biomechanical analysis.
