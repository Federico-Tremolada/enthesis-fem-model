# M14 – Power-Law Model (n = 2)

## Description

This model is part of the power-law sensitivity study carried out in Phase 2.

It uses a power-law material gradient with exponent n = 2 and a refined discretization of the enthesis region with 16 layers.

This model serves as a reference configuration previously identified in Phase 1.

## Geometry

* 2D planar rectangular model
* Total length: 30 mm
* Height: 6 mm
* Tendon region: 12 mm
* Enthesis region: 6 mm
* Bone region: 12 mm

## Interface Discretization

The enthesis region is discretized into 16 layers of equal thickness.

## Material Properties

### Tendon

* Young’s modulus: 200 MPa
* Poisson’s ratio: 0.45

### Bone

* Young’s modulus: 20000 MPa
* Poisson’s ratio: 0.30

### Enthesis

* Young’s modulus follows a power-law distribution
* exponent: n = 2
* Poisson’s ratio assumed constant

## Interface Modeling

The elastic modulus assigned to each enthesis layer is obtained from a power-law function evaluated at the center of each layer.

## Analysis Setup

* Software: Abaqus/CAE
* Model type: 2D planar
* Formulation: Plane Stress
* Step: Static, General
* NLGEOM: OFF

## Boundary Conditions

* Right edge (bone side): U1 = 0, U2 = 0
* Left edge (tendon side): imposed displacement U1 = 0.3 mm
* U2 free on the loaded side

## Mesh

* Element type: CPS4R
* Refined mesh in the enthesis region

## Purpose

This model serves as a reference to evaluate the effect of increasing the exponent beyond the baseline identified in Phase 1.

## Expected Behavior

The n = 2 configuration is expected to:

* provide a balanced stiffness transition
* reduce stress concentration compared to linear models
* produce a smoother stress distribution than lower exponents
