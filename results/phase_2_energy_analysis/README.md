# Phase 2 — Elastic Energy Analysis

This folder contains the results of the elastic energy analysis performed to investigate the relationship between stress distribution and energy storage along the tendon–bone interface.

---

## Models

* M17 → power-law (n = 3), constant Poisson’s ratio
* M18 → power-law (n = 3), variable Poisson’s ratio

---

## Files

* `S11_vs_SENER_M17.png` → combined plot of S11 and SENER along the centerline (M17)

* `S11_vs_SENER_M18.png` → combined plot of S11 and SENER along the centerline (M18)

* `SENER_comparison.png` → comparison of SENER(x) between M17 and M18

* `energy_summary.png` → comparison of total elastic energy (ALLSE)

* `energy_summary.csv` → numerical values of total energy, peaks and gradients

---

## Methodology

* Extraction of S11 and SENER fields from Abaqus (.odb)
* Projection along the centerline
* Numerical integration of SENER
* Identification of:

  * peak values
  * spatial gradients
  * correlation between stress and energy

---

## Key Results

### Energy Distribution

* SENER profiles are nearly identical for both models
* The transition zone is sharply localized
* No significant shift in position is observed

---

### Global Metrics

* Total energy:

  * M17 = 0.63598
  * M18 = 0.63604
    → negligible difference (~0.01%)

* Peak SENER:

  * nearly identical

* Maximum gradient:

  * slightly reduced in M18 (~5%)

---

### Stress–Energy Relationship

A strong spatial correlation is observed between:

* rapid variation of S11
* sharp decay of SENER

This identifies a well-defined **active interface region**, where load transfer occurs.

---

## Interpretation

* The mechanical response is governed primarily by the Young’s modulus gradient
* Poisson’s ratio affects only secondary deformation mechanisms
* The energy distribution is largely insensitive to Poisson’s ratio variation

---

## Key Insight

The location and intensity of energy concentration are controlled by stiffness variation, not by Poisson’s ratio.

---

## Conclusion

* Introducing a variable Poisson’s ratio does not significantly affect:

  * energy distribution
  * peak values
  * total stored energy

* A minor smoothing effect is observed, but it does not justify the added model complexity

---

## Outcome

The dominant design parameter in graded interfaces is the spatial variation of stiffness, while Poisson’s ratio plays a secondary role.

This result provides a clear guideline for simplified and efficient modeling strategies.
