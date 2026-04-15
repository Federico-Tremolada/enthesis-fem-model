# Phase 2 — Poisson’s Ratio Study

This folder contains the results of the analysis performed to evaluate the influence of Poisson’s ratio variation on the mechanical behavior of the interface.

The study compares a constant Poisson’s ratio model with a spatially varying Poisson’s ratio across the enthesis.

---

## Contents

* `S11_poisson_comparison.png` → comparison of S11 stress profiles

* `Mises_poisson_comparison.png` → comparison of von Mises stress profiles

* `Mises_peak_position_poisson.png` → position of maximum von Mises stress

* `summary_phaseC.csv` → extracted stress data

* `phaseC_final_table.csv` → summary of key metrics

---

## Models Included

* M17 → constant Poisson’s ratio
* M18 → variable Poisson’s ratio

Both models use:

* power-law material distribution (n = 3)
* 16-layer discretization
* identical geometry and boundary conditions

---

## Purpose

The aim of this study is to evaluate whether introducing a spatial variation of Poisson’s ratio significantly affects:

* stress distribution
* load transfer mechanisms
* overall mechanical response

---

## Interpretation

### S11 Profiles

* The stress profiles are nearly identical for both configurations
* Differences in peak values are minimal
* The overall shape of the distribution remains unchanged

---

### von Mises Profiles

* The stress distributions overlap almost completely
* No significant change in peak stress values is observed
* The global mechanical response is largely unaffected

---

### Peak Position Analysis

* The x-position of the maximum von Mises stress remains unchanged
* The y-position varies significantly between the two models

This indicates that Poisson’s ratio influences transverse deformation but does not affect the primary load transfer direction.

---

## Key Findings

* Poisson’s ratio variation has a negligible effect on stress distribution along the interface
* The dominant factor governing mechanical behavior is the Young’s modulus gradient
* Variations in Poisson’s ratio mainly affect secondary deformation characteristics

---

## Outcome

The introduction of a variable Poisson’s ratio does not significantly improve the mechanical performance of the model.

For this reason, further analyses focus primarily on material stiffness variation rather than Poisson’s ratio effects.

---

## Notes

This result supports the assumption that, in functionally graded interfaces, the spatial variation of Young’s modulus plays a more critical role than Poisson’s ratio in controlling stress transfer.
