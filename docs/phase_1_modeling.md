# Modeling Choices

This document describes and justifies the main modeling assumptions adopted in the FEM analysis of the tendon–bone interface.

The goal is to balance physical realism, computational efficiency, and interpretability of results.

---

## 1. Dimensionality of the Model

A **2D planar model** is used to represent the tendon–bone system.

### Rationale

* The main objective is to analyze stress transfer along the interface
* The problem is predominantly governed by longitudinal stress (S11)
* A 2D model allows:

  * faster simulations
  * easier parametric studies
  * clearer interpretation of results

### Implications

* Out-of-plane effects are neglected
* The model captures relative trends rather than exact 3D behavior

---

## 2. Plane Stress Assumption

The model is formulated under **plane stress conditions**.

### Rationale

* The structure is thin compared to its in-plane dimensions
* The dominant loading is applied along the longitudinal direction
* Plane stress is appropriate for thin biological tissues under tension

---

## 3. Geometry Simplification

A simplified rectangular geometry is adopted:

* Tendon region
* Enthesis (interface) region
* Bone region

### Rationale

* Focus is on material transition, not geometric complexity
* Simplified geometry allows controlled comparison between models
* Eliminates confounding effects due to shape irregularities

---

## 4. Material Modeling

Materials are modeled as **linear elastic**.

### Rationale

* Objective is to isolate the effect of material gradients
* Linear elasticity provides a first-order approximation
* Avoids introducing additional nonlinear parameters

### Limitations

* Real biological tissues are viscoelastic and anisotropic
* Nonlinear effects are not captured at this stage

---

## 5. Interface Discretization

The enthesis region is discretized into **8 layers**:

* 2 outer layers: 1.2 mm
* 6 inner layers: 0.6 mm

### Rationale

* Approximates a continuous material gradient
* Maintains low computational cost
* Provides sufficient resolution for stress variation

---

## 6. Material Gradient Laws

Different laws are used to define the variation of Young’s modulus:

* Sharp (discontinuous)
* Linear
* Exponential
* Power-law (n = 0.5, n = 2)

### Rationale

* Enable systematic comparison of transition behaviors
* Represent different stiffness evolution profiles:

  * linear → uniform transition
  * exponential → rapid stiffening
  * power-law → tunable gradient shape

---

## 7. Boundary Conditions

* Bone side: fully constrained (U1 = 0, U2 = 0)
* Tendon side: imposed displacement in longitudinal direction

### Rationale

* Mimics tensile loading of the tendon
* Represents bone as a rigid support
* Ensures consistent loading across all models

---

## 8. Mesh Strategy

* Element type: CPS4R
* Refined mesh in the enthesis region

### Rationale

* Reduced integration elements improve efficiency
* Mesh refinement captures stress gradients at the interface
* Ensures accuracy in critical regions

---

## 9. Choice of Output Quantity

The primary variable analyzed is **S11 (longitudinal stress)**.

### Rationale

* Directly related to load transfer across the interface
* Most relevant component under tensile loading
* Enables clear comparison between models

---

## 10. Modeling Philosophy

The modeling approach follows a **controlled simplification strategy**:

* keep geometry simple
* vary only one parameter (material law)
* isolate cause–effect relationships

### Objective

To identify how different material gradients influence:

* stress concentration
* load transfer
* mechanical compatibility

This provides a solid foundation for introducing more complex physics in subsequent phases of the project.
