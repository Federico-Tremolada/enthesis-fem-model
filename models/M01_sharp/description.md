# M01 – Sharp Interface

## Description

This model represents a sharp transition between tendon and bone, with no intermediate graded region.

## Geometry

- 2D planar rectangular model
- Total length: 30 mm
- Height: 6 mm
- Tendon region: 15 mm
- Bone region: 15 mm

## Material Properties

### Tendon
- Young’s modulus: 200 MPa
- Poisson’s ratio: 0.45

### Bone
- Young’s modulus: 20000 MPa
- Poisson’s ratio: 0.30

## Interface

The tendon–bone interface is modeled as a sharp discontinuity at x = 15 mm, with no gradual transition in elastic properties.

## Analysis Setup

- Software: Abaqus/CAE
- Model type: 2D planar
- Formulation: Plane Stress
- Step: Static, General
- NLGEOM: OFF

## Boundary Conditions

- Right edge (bone side): U1 = 0, U2 = 0
- Left edge (tendon side): imposed displacement U1 = 0.3 mm
- U2 free on the loaded side

## Mesh

- Element type: CPS4R
- Local mesh refinement near the interface

## Purpose

This model is the baseline configuration used to evaluate stress concentration effects due to abrupt elastic mismatch.

## Expected Behavior

Because of the sharp material discontinuity, the model is expected to show strong stress concentration near the tendon–bone interface.
