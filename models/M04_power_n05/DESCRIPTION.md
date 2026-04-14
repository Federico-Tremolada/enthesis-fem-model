# M04 – Power-Law Graded Interface (n = 0.5)

## Description

This model introduces a power-law variation of Young’s modulus across the tendon–bone interface with exponent n = 0.5, resulting in a concave gradient profile.

## Geometry

- 2D planar rectangular model
- Total length: 30 mm
- Height: 6 mm
- Tendon region: 12 mm
- Enthesis region: 6 mm
- Bone region: 12 mm

## Interface Discretization

The enthesis region is discretized into 8 layers:

- 2 outer layers: 1.2 mm each
- 6 inner layers: 0.6 mm each

This discretization is used to approximate a continuous power-law gradient.

## Material Properties

### Tendon
- Young’s modulus: 200 MPa
- Poisson’s ratio: 0.45

### Bone
- Young’s modulus: 20000 MPa
- Poisson’s ratio: 0.30

### Enthesis
- Young’s modulus follows a power-law distribution (n = 0.5)
- Poisson’s ratio initially assumed uniform

## Interface Modeling

The elastic modulus assigned to each enthesis layer follows a power-law function with exponent n = 0.5, producing a faster stiffness increase near the tendon region.

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
- Refined mesh in the enthesis region

## Purpose

This model is used to evaluate how a softer initial gradient influences stress transfer and concentration.

## Expected Behavior

Compared to linear and exponential models, this configuration is expected to:

- reduce stiffness mismatch near the tendon
- alter stress distribution along the interface
- potentially shift the location of peak stress

## Visuals

### Geometry
![Geometry](geometry.png)

### Mesh
![Mesh](mesh.png)

### Boundary Conditions
![Boundary Conditions](boundary_conditions.png)

### Stress Distribution (S11)
![S11](stress_S11.png)
