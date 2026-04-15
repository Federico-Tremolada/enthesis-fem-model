# Phase 1 — Key Results

This folder contains the main results of the first phase of the project, where different material transition laws are compared across the tendon–bone interface.

These results represent the primary basis for model evaluation and selection.

---

## Contents

* `S11_comparison_advanced.png` → global comparison of S11 stress profiles
* `S11_zoom_all_models.png` → zoomed view near the interface
* `summary_metrics_all.csv` → quantitative metrics (e.g., peak stress values)

---

## Purpose

The objective of this analysis is to evaluate how different material gradients influence:

* stress concentration at the interface
* smoothness of stress transfer
* overall mechanical response of the system

---

## Interpretation

* The sharp interface shows a strong stress concentration due to the abrupt stiffness mismatch
* Graded models improve stress redistribution by introducing a gradual transition
* Differences between gradient types become more evident near the interface region

The comparison highlights how the shape of the material law directly affects load transfer mechanisms.

---

## Key Findings

* The sharp interface exhibits the highest stress concentration
* The linear and exponential models reduce peak stress but still present relatively abrupt transitions
* The power-law model with n = 0.5 modifies the stress profile but does not significantly reduce peak values
* The power-law model with n = 2 provides the best balance between peak reduction and smooth stress distribution

---

## Role in the Project

These results guide the selection of the most effective material transition law.

The **power-law model with exponent n = 2** is chosen as the reference configuration for Phase 2, where further refinement and physical validation are performed.

---

## Notes

These plots represent the core results of Phase 1 and should be interpreted together with the advanced analyses provided in `phase_1_advanced_analysis/`, which offer additional insight into stress gradients and curvature.
