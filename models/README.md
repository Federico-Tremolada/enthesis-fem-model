# Models

This folder contains the finite element interface models developed in the project.

Each subfolder corresponds to a specific material transition law and includes:

- model description
- geometry image
- mesh image
- boundary conditions image
- S11 stress distribution image

Heavy Abaqus files such as `.cae` and `.odb` are not included in the repository.

## Model Comparison Overview

This section summarizes the interface models implemented in the first phase of the project.

| Model | Folder | Interface Type | Gradient Shape |
|------|------|------|------|
| M01 | `M01_sharp/` | Sharp interface | Discontinuous |
| M02 | `M02_linear/` | Graded interface | Linear |
| M03 | `M03_exponential/` | Graded interface | Exponential |
| M04 | `M04_power_n05/` | Graded interface | Power-law |
| M05 | `M05_power_n2/` | Graded interface | Power-law |

## Comparison Logic

All models share the same:

- geometry
- boundary conditions
- loading setup
- general finite element framework

The main variable changed across models is the material law assigned to the enthesis region.

This makes the comparison physically controlled and allows the effect of the interface law on stress transfer to be isolated.

## Role in the Project

These models were developed to compare different transition laws across the tendon–bone interface and identify the most effective one in terms of:

- reduction of stress concentration
- smoother stress redistribution
- more gradual load transfer

The power-law model with exponent **n = 2** was selected for the following phase of the project, where further physical improvements were introduced.
