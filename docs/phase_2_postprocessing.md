# Phase 2 — Post-processing and Analysis

## Introduction

This phase focuses on the quantitative evaluation of the refined models developed in Phase 2.

The objective is to assess the mechanical behavior of the tendon–bone interface using both:

* stress-based metrics
* energy-based metrics

This combined approach provides a more robust and physically meaningful interpretation of the results.

---

## 1. Stress Distribution Analysis

### Method

Stress profiles are extracted along a line crossing the tendon–bone interface.

The primary quantity of interest is:

* longitudinal stress (S11)

Data is obtained from Abaqus output databases (.odb) and processed using Python.

---

### Observations

The comparison between models highlights:

* smoother stress transitions with increased layer refinement
* reduced stress concentration for higher power-law exponents
* minimal influence of Poisson’s ratio variation

In particular:

* the 16-layer configuration reduces numerical discontinuities
* the power-law model with n = 3 provides the most uniform stress distribution

---

### Interpretation

The results confirm that:

* abrupt stiffness changes lead to localized stress peaks
* gradual stiffness transitions improve load transfer
* delayed stiffening (higher exponent) enhances mechanical compatibility

---

## 2. Elastic Energy Analysis

### Theoretical Background

The elastic strain energy represents the energy stored in the material due to deformation.

It is defined as:

[
U = \int_V \frac{1}{2} , \sigma : \varepsilon , dV
]

In finite element simulations, this quantity is directly available as:

* strain energy density (SENER)

---

### Method

* SENER is extracted from Abaqus
* values are evaluated along the interface
* comparison is performed between:

  * constant Poisson model
  * variable Poisson model

---

### Observations

The analysis shows:

* similar energy distributions between the two models
* no significant variation in peak energy values
* consistent spatial trends

---

### Interpretation

These results indicate that:

* elastic energy distribution is primarily governed by stiffness variation
* Poisson’s ratio has a secondary effect in this configuration

The agreement between stress-based and energy-based analysis strengthens the reliability of the model.

---

## 3. Correlation Between Stress and Energy

A direct comparison between S11 and SENER reveals:

* regions of high stress correspond to higher energy concentration
* smoother stress gradients lead to more distributed energy storage

This confirms that:

* reducing stress concentration also reduces localized energy accumulation
* graded interfaces improve mechanical efficiency

---

## 4. Consistency with FGM Theory

The observed behavior is consistent with theoretical expectations for functionally graded materials:

* gradual variation of material properties reduces stress discontinuities
* convex gradients (higher power-law exponents) improve load transfer
* energy is more evenly distributed across the interface

---

## 5. Key Findings

The post-processing analysis leads to the following conclusions:

* increasing discretization improves numerical and physical accuracy

* the power-law exponent significantly influences stress distribution

* the optimal configuration is:

  * 16 layers
  * power-law exponent n = 3

* Poisson’s ratio variation has a negligible impact

* energy-based metrics confirm stress-based observations

---

## 6. Final Model Validation

The selected model demonstrates:

* reduced stress concentration
* smooth stress transfer
* consistent energy distribution
* agreement with FGM theory

This confirms its suitability for further development and potential scientific reporting.

---

## Role in the Project

This phase provides the final validation of the modeling strategy by:

* confirming the robustness of the selected configuration
* supporting conclusions with multiple physical metrics
* connecting numerical results to established theory

It represents the final step before transitioning to formal scientific communication.
