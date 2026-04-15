# Models

This folder contains all finite element models developed throughout the project.

Each subfolder corresponds to a specific model configuration and includes:

* model description (`DESCRIPTION.md`)
* geometry image
* mesh image
* boundary conditions image
* S11 stress distribution image

Heavy Abaqus files such as `.cae` and `.odb` are not included in the repository.

---

## Phase 1 — Interface Model Comparison

This phase focuses on comparing different material transition laws across the tendon–bone interface.

| Model | Folder             | Interface Type   | Gradient Shape |
| ----- | ------------------ | ---------------- | -------------- |
| M01   | `M01_sharp/`       | Sharp interface  | Discontinuous  |
| M02   | `M02_linear/`      | Graded interface | Linear         |
| M03   | `M03_exponential/` | Graded interface | Exponential    |
| M04   | `M04_power_n05/`   | Graded interface | Power-law      |
| M05   | `M05_power_n2/`    | Graded interface | Power-law      |

### Outcome

The power-law model with exponent **n = 2** was identified as the most effective configuration for reducing stress concentration and ensuring smooth load transfer.

---

## Phase 2 — Model Refinement and Sensitivity

This phase builds upon the selected configuration from Phase 1 and introduces progressive improvements.

---

### Refinement Study

| Model | Folder               | Layers |
| ----- | -------------------- | ------ |
| M10   | `M10_refinement_8/`  | 8      |
| M11   | `M11_refinement_12/` | 12     |
| M12   | `M12_refinement_16/` | 16     |

**Outcome:**

The 16-layer configuration provides a smoother stress distribution and better approximates a continuous material gradient.

---

### Power-Law Sensitivity

| Model | Folder            | Exponent (n) |
| ----- | ----------------- | ------------ |
| M13   | `M13_power_n1p5/` | 1.5          |
| M14   | `M14_power_n2/`   | 2            |
| M15   | `M15_power_n3/`   | 3            |
| M16   | `M16_power_n5/`   | 5            |

**Outcome:**

The model with **n = 3** provides the best balance between:

* stress reduction
* smooth load transfer
* mechanical consistency

---

### Poisson’s Ratio Study

| Model | Folder             | Poisson’s Ratio |
| ----- | ------------------ | --------------- |
| M17   | `M17_const_nu/`    | Constant        |
| M18   | `M18_variable_nu/` | Variable        |

**Outcome:**

The variation of Poisson’s ratio has a negligible influence on stress distribution compared to Young’s modulus variation.

---

## Comparison Logic

All models share the same:

* geometry
* boundary conditions
* loading setup
* finite element formulation

Only one parameter is modified at a time, ensuring a controlled comparison and isolating the effect of each modeling choice.

---

## Role in the Project

These models represent a progressive investigation of the mechanical behavior of the tendon–bone interface.

The modeling strategy follows a structured approach:

1. identify the most effective material law (Phase 1)
2. refine and validate the selected configuration (Phase 2)

The final selected model is:

* power-law distribution
* exponent n = 3
* refined discretization (16 layers)

This configuration is used for further physical validation and analysis in the subsequent stages of the project.
