# Phase 1 — Advanced Analysis

This folder contains additional post-processing analyses performed on the models developed in Phase 1.

These analyses provide a deeper interpretation of the mechanical behavior of different interface configurations beyond standard stress comparison.

---

## Contents

* `stress_gradient_comparison.png` → first spatial derivative of S11 along the interface
* `stress_curvature_comparison.png` → second spatial derivative of S11 along the interface

---

## Purpose

The objective of this analysis is to evaluate how the stress field evolves across the tendon–bone interface by examining:

* the rate of stress variation (gradient)
* the smoothness of the transition (curvature)

These metrics provide additional insight into load transfer mechanisms and the effectiveness of different material gradients.

---

## Interpretation

* High stress gradients indicate abrupt changes and potential stress concentration
* Lower gradients suggest smoother load transfer
* Curvature highlights how rapidly the stress profile changes shape along the interface

Together, these quantities help distinguish between different graded models at a more detailed level than standard stress plots.

---

## Role in the Project

This analysis supports the conclusions drawn from the main results of Phase 1 and reinforces the selection of the power-law model (n = 2) as the most effective configuration.

It provides additional evidence that functionally graded transitions improve mechanical behavior compared to sharp interfaces.

---

## Notes

These plots are intended as advanced interpretation tools and should be considered complementary to the main S11 comparison figures contained in `phase_1_key_results/`.
