# Results

This folder contains the processed outputs derived from the finite element simulations of the tendon–bone interface.

The results are organized according to the different phases of the project, each addressing a specific aspect of the mechanical behavior of graded interfaces.

---

## Structure

* `phase_1_key_results/` → baseline comparison between different material transition laws

* `phase_1_advanced_analysis/` → derivative-based and refined analyses of Phase 1

* `phase_2_refinement/` → mesh and discretization sensitivity (layer refinement)

* `phase_2_n_sensitivity/` → influence of power-law exponent (n) on stress distribution

* `phase_2_poisson/` → effect of Poisson’s ratio variation

* `phase_2_energy_analysis/` → elastic energy analysis and stress–energy correlation

---

## Phase Overview

### Phase 1 — Baseline Comparison

Objective:
Evaluate how different material transition laws (sharp, linear, exponential, power-law) affect stress distribution.

Outputs:

* S11(x) profiles
* von Mises stress maps
* qualitative comparison of stress concentration

---

### Phase 2 — Model Development and Validation

This phase focuses on refining the most promising model (power-law) and assessing the influence of key parameters.

---

#### 2.1 Refinement

Objective:
Assess the influence of the number of layers used to discretize the graded region.

Outputs:

* comparison between different discretizations (e.g. 8 vs 16 layers)
* evaluation of numerical convergence and stability

---

#### 2.2 Power-Law Sensitivity (n)

Objective:
Evaluate how the exponent of the power-law affects stress distribution and load transfer.

Outputs:

* S11(x) comparison for different values of n
* von Mises profiles
* peak stress values and their spatial position

Key insight:
The exponent n strongly influences stress smoothness and peak localization, with an optimal balance observed around n = 3.

---

#### 2.3 Poisson’s Ratio Study

Objective:
Assess the effect of introducing a spatially varying Poisson’s ratio.

Outputs:

* comparison of S11(x) and von Mises(x)
* analysis of peak position in both x and y directions

Key insight:
Poisson’s ratio variation has a negligible effect on stress distribution along the interface, affecting mainly transverse deformation.

---

#### 2.4 Elastic Energy Analysis

Objective:
Investigate the relationship between stress distribution and energy storage using the elastic energy density (SENER).

Outputs:

* SENER(x) profiles
* comparison with S11(x)
* total elastic energy (ALLSE)
* peak values and gradients

Key insight:

* Strong spatial correlation between stress variation and energy distribution
* Energy localization identifies the active load transfer region
* The mechanical response is governed primarily by the Young’s modulus gradient

---

## Main Outputs

The most relevant results across the project include:

* S11(x) profiles → primary indicator of stress transfer along the interface
* von Mises stress → global mechanical response
* SENER(x) → energy-based interpretation of load transfer

---

## Purpose

This folder provides a structured and consistent organization of all processed results, enabling:

* clear comparison between models
* physical interpretation of stress and energy distributions
* direct integration into scientific reports and manuscript preparation

---
