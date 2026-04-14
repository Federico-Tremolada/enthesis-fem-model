# Phase 2 — Overview

## Objective

The second phase of the project aims to improve the physical reliability and robustness of the tendon–bone interface model developed in Phase 1.

While Phase 1 focused on identifying an effective material transition law, Phase 2 extends the analysis by:

* increasing spatial resolution
* refining the material gradient
* introducing additional physical effects
* validating the model using energy-based metrics
* comparing results with established trends in functionally graded materials (FGMs)

---

## Background

Phase 1 identified the **power-law model with exponent n = 2** as the most effective configuration for reducing stress concentration and ensuring smooth load transfer.

However, this result is based on:

* a relatively coarse discretization of the interface
* a fixed material law
* simplified material assumptions

Phase 2 addresses these limitations by systematically refining the model.

---

## Strategy

The phase is structured as a sequence of controlled sub-steps, each designed to isolate a specific modeling aspect.

Only one parameter is modified at a time, ensuring that cause–effect relationships remain clear and interpretable.

---

## Sub-Phases

### 1. Interface Refinement

The number of layers in the enthesis region is increased to evaluate the effect of spatial discretization on stress distribution.

**Goal:**
Improve the resolution of the material gradient and assess convergence behavior.

---

### 2. Sensitivity to Power-Law Exponent

The exponent of the power-law is varied to understand how the shape of the material gradient influences stress transfer.

**Goal:**
Identify the exponent that provides the optimal balance between stress reduction and smooth transition.

---

### 3. Effect of Poisson’s Ratio

A spatial variation of Poisson’s ratio is introduced to account for transverse deformation effects.

**Goal:**
Evaluate whether this additional physical detail significantly influences stress distribution.

---

### 4. Elastic Energy Analysis

An energy-based approach is introduced using strain energy density.

**Goal:**
Provide an additional validation criterion beyond stress-based metrics.

---

### 5. Scientific Validation

Results are compared with theoretical and numerical trends reported in the literature on functionally graded materials.

**Goal:**
Assess the consistency of the model with established physical principles.

---

## Methodological Principles

The phase follows a set of key principles:

* isolate one variable at a time
* maintain consistent geometry and boundary conditions
* ensure comparability between models
* combine qualitative and quantitative analysis

---

## Expected Outcomes

Phase 2 aims to:

* identify a refined and physically consistent model configuration
* validate the selected material gradient
* strengthen the mechanical interpretation of results
* provide a solid basis for scientific reporting

---

## Role in the Overall Project

Phase 2 represents the transition from:

* exploratory modeling (Phase 1)
  to
* physically validated modeling

It significantly increases the credibility and robustness of the results, making the model suitable for further development and potential publication.
