# Phase 2 — Modeling Strategy

## Introduction

This phase builds upon the results of Phase 1, where the power-law model with exponent n = 2 was identified as the most effective material distribution.

The objective of Phase 2 is to improve the model by refining:

* spatial discretization
* material law parameters
* physical realism

All modifications are introduced progressively, ensuring controlled comparisons.

---

## Reference Configuration

All Phase 2 models are based on the same reference setup:

* 2D planar geometry
* Plane stress formulation
* Identical boundary conditions
* Same tendon and bone properties

The only modifications concern the **enthesis region**.

---

## 1. Interface Refinement

### Models

* M10 → 8 layers (baseline from Phase 1)
* M11 → 12 layers
* M12 → 16 layers

All models use:

* power-law distribution
* exponent n = 2

---

### Objective

To evaluate whether increasing the number of layers improves:

* smoothness of stress distribution
* numerical stability
* representation of the material gradient

---

### Implementation

The enthesis thickness remains constant, while the number of layers is increased.

This results in:

* thinner individual layers
* a closer approximation to a continuous gradient

Material properties are assigned using the same power-law function evaluated at the center of each layer.

---

### Outcome

The model with **16 layers (M12)** provides:

* smoother stress profiles
* reduced numerical artifacts
* better representation of a continuous transition

This configuration is selected for the next step.

---

## 2. Sensitivity to Power-Law Exponent

### Models

* M13 → n = 1.5
* M14 → n = 2
* M15 → n = 3
* M16 → n = 5

All models use:

* 16 enthesis layers

---

### Objective

To analyze how the exponent of the power-law affects:

* stress concentration
* stiffness distribution
* load transfer behavior

---

### Physical Interpretation

The exponent controls how quickly stiffness increases across the interface:

* lower n → rapid stiffening near tendon
* higher n → delayed stiffening, smoother transition

---

### Outcome

The model with **n = 3 (M15)** provides:

* lower stress peaks
* smoother stress gradients
* improved load transfer

This configuration is selected for further refinement.

---

## 3. Effect of Poisson’s Ratio

### Models

* M17 → constant Poisson’s ratio
* M18 → variable Poisson’s ratio

Both models use:

* 16 layers
* power-law exponent n = 3

---

### Objective

To evaluate the influence of transverse deformation on stress distribution.

---

### Implementation

In the variable model:

* Poisson’s ratio varies across the interface
* values transition between tendon and bone

---

### Outcome

The comparison shows:

* minimal differences in stress distribution
* negligible influence on peak values

This suggests that, for this configuration:

* Young’s modulus variation dominates the mechanical response

---

## Modeling Summary

The progressive refinement leads to the following final configuration:

* 16 enthesis layers
* power-law exponent n = 3
* constant Poisson’s ratio

---

## Key Modeling Principles

Throughout this phase, the following principles are maintained:

* one variable modified at a time
* consistent boundary conditions
* identical geometry across models
* direct comparability between configurations

---

## Transition to Analysis

The models defined in this phase are used for:

* stress-based comparison
* energy-based validation
* physical interpretation of graded interfaces

These aspects are addressed in the next document.
