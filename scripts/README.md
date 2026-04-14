# Scripts

This folder contains the scripts used for post-processing and analysis of the FEM simulations.

## Structure

- `python/` → data extraction and preprocessing
- `matlab/` → data analysis and advanced visualization

## Workflow

The post-processing pipeline follows these steps:

1. **Abaqus**
   - Simulation results are stored in `.odb` files

2. **Python**
   - Extract stress data from `.odb`
   - Generate CSV files
   - Compute summary metrics

3. **MATLAB / Python**
   - Compare models
   - Generate plots
   - Analyze stress distributions

## Python Scripts

- `extract_summary.py` → extracts global stress metrics from Abaqus results
- `extract_line_S11.py` → extracts S11 along the interface
- `analyze_S11_all.py` → compares all models and generates final plots

## MATLAB Scripts

- `plot_S11_comparison.m` → visual comparison of stress distributions
- `advanced_analysis.m` → gradient and curvature analysis
- `metrics_analysis.m` → quantitative comparison between models

## Notes

CSV files used as input are generated from Abaqus post-processing and stored in the `results/` folder.
