# Phase 2 — Power-Law Sensitivity Study

This folder contains the results of the sensitivity analysis performed on the exponent of the power-law material distribution.

The objective is to evaluate how different gradient shapes influence stress distribution across the tendon–bone interface.

---

## Contents

* `S11_n_sensitivity_comparison.png` → comparison of stress profiles for different exponents
* `S11_n_sensitivity_zoom.png` → zoomed view near the interface
* `summary_n_sensitivity.csv` → extracted stress data
* `comparison_metrics_n.csv` → quantitative comparison between models

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

The aim of this study is to evaluate how the shape of the material gradient affects:

* stress concentration
* smoothness of load transfer
* mechanical compatibility between tendon and bone

---

## Interpretation

* Lower exponents (n = 1.5) lead to a rapid increase in stiffness near the tendon side
* Higher exponents (n = 5) delay the stiffness increase toward the bone side
* Intermediate values provide a more balanced transition

These differences strongly influence the stress distribution along the interface.

---

## Key Findings

* The exponent significantly affects the stress profile
* n = 1.5 shows higher stress concentration near the interface
* n = 5 produces a delayed but less uniform stress transfer
* n = 2 improves the distribution compared to lower exponents
* n = 3 provides the best balance between smoothness and stress reduction

---

## Outcome

The configuration with **n = 3 (M15)** is selected as the reference model for the subsequent analyses.

This choice ensures:

* reduced stress concentration
* smooth and gradual load transfer
* physically consistent material transition

---

## Notes

This study highlights the importance of the material law in controlling mechanical behavior, showing that not only the presence of a gradient, but also its shape, plays a critical role.
