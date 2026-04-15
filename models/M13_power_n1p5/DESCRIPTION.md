# M13 – Power-Law Model (n = 1.5)

## Description

This model is part of the power-law sensitivity study carried out in Phase 2.

It uses a power-law material gradient with exponent n = 1.5 and a refined discretization of the enthesis region with 16 layers.

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
* exponent: n = 1.5
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

This model is used to evaluate the effect of a lower power-law exponent on stress distribution.

## Expected Behavior

Compared to higher exponents, the n = 1.5 configuration is expected to:

* increase stiffness more rapidly near the tendon region
* produce higher stress concentration close to the interface
* result in a less smooth stress distribution
