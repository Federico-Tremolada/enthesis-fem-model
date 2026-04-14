# Key Results

This folder contains the main post-processing results used to compare the stress distribution across different interface models.

## Contents

- `S11_comparison_advanced.png` → global comparison of S11 stress along the full normalized line
- `S11_zoom_all_models.png` → zoomed comparison near the interface
- `summary_metrics_all.csv` → summary table with quantitative metrics for each model

## Compared models

- Sharp interface
- Linear gradient
- Exponential gradient
- Power-law gradient (n = 0.5)
- Power-law gradient (n = 2)

## Purpose

These results are used to identify which material law provides the smoothest stress transfer and the lowest local stress concentration near the tendon–bone interface.

## Interpretation of Results

The comparison of S11 stress distributions shows clear differences between the interface models.

- The **sharp interface** exhibits the highest stress concentration near the interface.
- The **linear model** reduces the peak but still shows a relatively abrupt stress transition.
- The **exponential model** provides a smoother redistribution of stress.
- The **power-law model (n = 0.5)** modifies the stress profile but does not significantly reduce peak concentration.
- The **power-law model (n = 2)** achieves the best balance between peak stress reduction and smooth stress transfer.

## Model Selection

Based on the observed results, the **power-law model with n = 2** is selected for further development.

This choice is motivated by:

- reduced stress concentration
- smoother gradient across the interface
- improved mechanical compatibility between regions
