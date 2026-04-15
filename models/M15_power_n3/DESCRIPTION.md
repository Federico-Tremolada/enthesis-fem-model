# M15 – Power-Law Model (n = 3)

## Description

This model is part of the power-law sensitivity study carried out in Phase 2.

It uses a power-law material gradient with exponent n = 3 and a refined discretization of the enthesis region with 16 layers.

This model is selected as the optimal configuration based on its stress distribution performance.

## Geometry

* 2D planar rectangular model
* Total length: 30 mm
* Height: 6 mm
* Tendon region: 12 mm
* Enthesis region: 6 mm
* Bone region: 12 mm

## Interface Discretization

The enthesis region is discretized into 16 layers of equal thickness.

This uniform discretization allows for a consistent comparison between different power-law exponents.

## Material Properties

### Tendon

* Young’s modulus: 200 MPa
* Poisson’s ratio: 0.45

### Bone

* Young’s modulus: 20000 MPa
* Poisson’s ratio: 0.30

### Enthesis

* Young’s modulus follows a power-law distribution
* exponent: n = 3
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

This model is used to evaluate the effect of increasing the power-law exponent on stress distribution across the interface.

## Expected Behavior

Compared to lower exponents, the n = 3 configuration is expected to:

* delay stiffness increase across the interface
* reduce stress concentration near the tendon side
* produce a smoother stress gradient

## Visuals

### Geometry

![Geometry](geometry.png)

### Mesh

![Mesh](mesh.png)

### Boundary Conditions

![Boundary Conditions](boundary_conditions.png)

### Stress Distribution (S11)

![S11](stress_S11.png)
