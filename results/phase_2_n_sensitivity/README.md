# Phase 2 — Power-Law Sensitivity Study

This folder contains the results of the sensitivity analysis performed on the exponent of the power-law material distribution.

The objective is to evaluate how different gradient shapes influence stress distribution and load transfer across the tendon–bone interface.

---

## Contents

* `S11_n_sensitivity_comparison.png` → comparison of S11 stress profiles

* `Mises_n_sensitivity_comparison.png` → comparison of von Mises stress profiles

* `Mises_peak_position.png` → position of maximum von Mises stress along the interface

* `summary_phaseB.csv` → extracted stress data

* `phaseB_final_table.csv` → summary of key metrics

---

## Models Included

* M13 → n = 1.5
* M14 → n = 2
* M15 → n = 3
* M16 → n = 5

All models use:

* 16-layer discretization
* identical geometry and boundary conditions

---

## Purpose

The aim of this study is to assess how the shape of the material gradient affects:

* stress concentration
* smoothness of load transfer
* spatial distribution of stresses

---

## Interpretation

### S11 Profiles

* Lower exponents (n = 1.5) show sharper stress variations near the interface
* Increasing n leads to a smoother and more distributed stress profile
* High values (n = 5) shift the stress concentration further into the interface

---

### von Mises Profiles

* The overall stress level decreases as n increases
* Higher exponents lead to a broader and more distributed stress field
* This suggests improved load sharing across the interface

---

### Peak Position Analysis

* The position of maximum von Mises stress shifts toward the bone side as n increases
* This indicates a progressive redistribution of load along the interface
* The shift is approximately monotonic with increasing exponent

---

## Key Findings

* The exponent of the power-law strongly influences stress distribution
* n = 1.5 leads to higher stress concentration near the tendon side
* n = 5 delays stress transfer excessively
* n = 2 improves stress distribution compared to lower exponents
* n = 3 provides the best balance between stress reduction and smooth load transfer

---

## Outcome

The configuration with **n = 3 (M15)** is selected as the reference model for the subsequent analyses.

This choice ensures:

* reduced stress concentration
* smooth stress redistribution
* physically consistent load transfer

---

## Notes

This analysis demonstrates that the effectiveness of a graded interface depends not only on the presence of a material gradient, but also on its shape.

The exponent of the power-law plays a critical role in controlling the mechanical response of the system.

