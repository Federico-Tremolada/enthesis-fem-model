# Enthesis FEM Model – Stress Distribution in Functionally Graded Interfaces

## Overview

The tendon-to-bone interface (enthesis) is a complex biological structure characterized by a gradual transition of mechanical properties from soft tendon to stiff bone.

This project investigates how different material distributions affect stress concentration at the interface using Finite Element Modeling (FEM).

The objective is to evaluate whether functionally graded materials (FGMs) reduce stress peaks compared to sharp interfaces.

---

## Problem Statement

In many engineered systems, abrupt changes in material properties lead to stress concentrations and potential failure.

In contrast, biological systems often adopt gradual transitions to mitigate these effects.

The enthesis is a prime example of this strategy.

This project aims to:

- model the tendon–bone interface
- introduce different material gradients
- analyze stress distribution along the interface
- evaluate the mechanical advantage of graded transitions

---

## Model Description

A simplified 2D/3D FEM model is used:

- Tendon region → low stiffness
- Bone region → high stiffness
- Interface (enthesis) → graded material properties

Different configurations are implemented:

- Sharp interface (baseline)
- Linear gradient
- Exponential gradient
- Power-law gradient

Material properties vary along the interface according to predefined laws.

---

## Methodology

The project follows a structured simulation pipeline:

### Phase A — Model Generation (Abaqus)

- Geometry definition
- Material assignment
- Mesh generation
- Boundary conditions

### Phase B — Post-processing (Python)

- Extraction of:
  - S11 stress
  - von Mises stress
  - stress profiles along the interface
- Export to CSV

### Phase C — Data Analysis (MATLAB / Python)

- Comparison between models
- Stress peak evaluation
- Distribution analysis

### Phase D — Advanced Validation

- Elastic energy analysis
- Correlation between stress and energy
- Comparison with literature trends on FGMs

---

## Results (Work in Progress)

Preliminary observations:

- Sharp interfaces show strong stress concentrations
- Graded models redistribute stress more smoothly
- Power-law gradients appear to reduce peak stresses more effectively

Further quantitative analysis is ongoing.

---

## Repository Structure

```text
docs/      → technical documentation
models/    → FEM model descriptions and screenshots
scripts/   → Python/MATLAB post-processing
results/   → processed data and plots
paper/     → manuscript and figures
