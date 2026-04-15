# Phase 2 — Refinement Study

This folder contains the results of the refinement study performed in Phase 2.

The objective of this analysis is to evaluate the effect of increasing the number of layers in the enthesis region on stress distribution and numerical convergence.

---

## Contents

* `S11_refinement_comparison.png` → comparison of stress profiles for different discretizations
* `summary_layers.csv` → extracted stress data along the interface
* `comparison_metrics.csv` → quantitative comparison between models
* `convergence_report.txt` → automatic convergence evaluation

---

## Models Included

* M10 → 8 layers (L08)
* M11 → 12 layers (L12)
* M12 → 16 layers (L16)

All models use:

* power-law material distribution
* exponent n = 2
* identical geometry and boundary conditions

---

## Purpose

The aim of this study is to assess how spatial discretization affects:

* smoothness of stress distribution
* numerical convergence
* accuracy in representing the material gradient

---

## Interpretation

* Increasing the number of layers improves the resolution of the material gradient
* The 8-layer model shows more pronounced discretization effects
* The 12-layer and 16-layer models produce very similar stress profiles

Differences between L12 and L16 are minimal and mainly visible near the interface region.

---

## Quantitative Analysis

The comparison between models shows:

* variations below ~2% for stress metrics between L12 and L16
* negligible differences in peak stress values
* strong convergence of the solution with increasing refinement

---

## Key Findings

* The solution converges as the number of layers increases
* The 12-layer and 16-layer models provide nearly identical results
* The 8-layer model is slightly less accurate but still consistent

---

## Outcome

The configuration with **16 layers (M12)** is selected for the subsequent analyses.

This choice ensures:

* maximum spatial resolution
* robustness for further sensitivity studies
* consistency with a high-fidelity representation of the graded interface

---

## Notes

Although the 12-layer model provides comparable results with lower computational cost, the 16-layer configuration is preferred to ensure higher numerical accuracy and avoid discretization-related artifacts in subsequent analyses.
