# Phase 2 — Refinement Study

This folder contains the results of the refinement study performed in Phase 2.

The objective of this analysis is to evaluate the effect of increasing the number of layers in the enthesis region on stress distribution.

---

## Contents

* `S11_refinement_comparison.png` → comparison of stress profiles for different discretizations
* `S11_refinement_zoom.png` → zoomed view near the interface
* `summary_metrics_refinement.csv` → quantitative comparison of stress metrics

---

## Models Included

* M10 → 8 layers
* M11 → 12 layers
* M12 → 16 layers

All models use:

* power-law material distribution
* exponent n = 2
* identical geometry and boundary conditions

---

## Purpose

The aim of this study is to assess how spatial discretization affects:

* smoothness of stress distribution
* numerical stability
* accuracy in representing the material gradient

---

## Interpretation

* Increasing the number of layers improves the resolution of the material gradient
* Coarser models (8 layers) show more irregular stress profiles
* Finer models (16 layers) produce smoother and more continuous stress distributions

The differences are most evident near the interface region.

---

## Key Findings

* The 8-layer model provides a reasonable approximation but shows discretization effects
* The 12-layer model improves smoothness and reduces irregularities
* The 16-layer model offers the best representation of a continuous gradient

---

## Outcome

The configuration with **16 layers (M12)** is selected for the subsequent analyses.

This choice ensures:

* improved numerical accuracy
* smoother stress transfer
* better representation of the physical behavior of a graded interface

---

## Notes

These results represent the first step of Phase 2 and establish the spatial discretization used in all subsequent analyses.
