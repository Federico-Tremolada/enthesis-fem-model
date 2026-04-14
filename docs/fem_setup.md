# FEM Setup

This document describes the technical implementation of the finite element models used in the analysis of the tendon–bone interface.

---

## 1. Software

* **Software:** Abaqus/CAE
* **Analysis type:** Static, General
* **Solver:** Standard (implicit)

---

## 2. Model Type

* **Dimensionality:** 2D planar
* **Formulation:** Plane Stress
* **Nonlinear geometry (NLGEOM):** OFF

### Rationale

* Small deformation assumption
* Focus on material-induced stress distribution rather than geometric nonlinearities

---

## 3. Geometry

The model consists of three regions:

* **Tendon**
* **Enthesis (interface)**
* **Bone**

### Dimensions

* Total length: 30 mm
* Height: 6 mm

Subdivision:

* Tendon: 12 mm
* Enthesis: 6 mm
* Bone: 12 mm

---

## 4. Materials

### Tendon

* Young’s modulus: 200 MPa
* Poisson’s ratio: 0.45

### Bone

* Young’s modulus: 20000 MPa
* Poisson’s ratio: 0.30

### Enthesis

* Young’s modulus varies according to the selected gradient law
* Poisson’s ratio initially assumed constant

---

## 5. Element Type

* **Element:** CPS4R

  * 4-node bilinear plane stress quadrilateral
  * Reduced integration

### Rationale

* Good balance between accuracy and computational cost
* Suitable for large parametric studies

---

## 6. Mesh Strategy

* Structured mesh across the entire domain
* Local refinement in the enthesis region

### Objective

* Capture high stress gradients near the interface
* Ensure numerical stability and accuracy

---

## 7. Boundary Conditions

### Bone Side (Right Edge)

* U1 = 0
* U2 = 0

### Tendon Side (Left Edge)

* Prescribed displacement:

  * U1 = 0.3 mm
* U2 = free

### Rationale

* Simulates tensile loading of the tendon
* Represents bone as a rigid constraint

---

## 8. Loading Conditions

* Displacement-controlled loading
* Applied along the longitudinal direction (x-axis)

### Advantages

* Stable numerical behavior
* Direct control over deformation level

---

## 9. Output Requests

The following field outputs are considered:

* **S11** → longitudinal stress
* **S, Mises** → equivalent stress (optional)

### Extraction Strategy

* Stress profiles are extracted along a line passing through the interface
* Data is exported for post-processing

---

## 10. Assumptions and Limitations

* Linear elastic material behavior
* No time-dependent effects
* No damage or failure modeling
* 2D approximation of a 3D biological structure

---

## 11. Modeling Consistency

All models share identical:

* geometry
* mesh
* boundary conditions
* loading

Only the material law in the enthesis region is varied.

### Purpose

To isolate the effect of material gradients on stress distribution.

---

## Summary

The FEM setup is designed to:

* ensure controlled comparison between models
* capture stress transfer across the interface
* provide reliable data for post-processing and analysis
