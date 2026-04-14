# M12 – Refinement Model (16 Layers)

## Description

This model is part of the refinement study carried out in Phase 2.

It uses a power-law material gradient with exponent n = 2 and increases the discretization of the enthesis region to 16 layers in order to better approximate a continuous transition.

## Geometry

* 2D planar rectangular model
* Total length: 30 mm
* Height: 6 mm
* Tendon region: 12 mm
* Enthesis region: 6 mm
* Bone region: 12 mm

## Interface Discretization

The enthesis region is discretized into 16 layers.

This refinement improves the spatial resolution of the material gradient and reduces discretization artifacts compared to coarser models.

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
* Poisson’s ratio initially assumed constant

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
* Higher spatial resolution compared to M10 and M11

## Purpose

This model is used to evaluate the effect of increasing the number of enthesis layers on stress distribution and numerical smoothness.

## Expected Behavior

Compared to coarser refinement models, the 16-layer configuration is expected to:

* better approximate a continuous material gradient
* reduce numerical discontinuities
* provide a smoother stress distribution

## Visuals

### Geometry

![Geometry](geometry.png)

### Mesh

![Mesh](mesh.png)

### Boundary Conditions

![Boundary Conditions](boundary_conditions.png)

### Stress Distribution (S11)

![S11](stress_S11.png)
