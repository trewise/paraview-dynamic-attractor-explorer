# Dynamic Attractor Observatory — Final Portfolio Writeup

## Overview

Dynamic Attractor Observatory is a reproducible scientific visualization project built around nonlinear dynamical systems and ParaView-compatible data generation.

The project simulates chaotic attractors, exports scientific data products, validates generated datasets, builds parameter sweeps, and prepares visualization scripts for ParaView.

## Why This Project Matters

Chaotic systems are visually rich and technically meaningful. They require careful numerical integration, structured data export, reproducibility, and clear visual communication. This project connects mathematical simulation with professional scientific visualization workflows.

## Core Pipeline

1. Attractor system definitions are selected from a registry.
2. A fixed-step RK4 solver integrates the system.
3. Trajectory data is exported to CSV.
4. ParaView-ready trajectory and point-cloud VTP files are generated.
5. Density VTI volumes are generated for volume rendering.
6. Metadata JSON files and YAML manifests document the outputs.
7. Parameter sweeps generate controlled variations.
8. Comparison datasets combine multiple attractors.
9. Preview assets and ParaView scripts support final portfolio presentation.

## Baseline Attractors

The project includes:

- Aizawa
- Chen
- Dadras
- Four-Wing
- Halvorsen
- Lorenz
- Rossler
- Sprott A
- Sprott B
- Sprott C
- Thomas

## Demonstrated Skills

- Python engineering
- Numerical methods
- Scientific computing
- Nonlinear dynamics
- VTK and ParaView data preparation
- Data validation
- Test-driven project workflow
- Automated build scripting
- Portfolio presentation

## Next Improvement

The strongest next improvement is to use ParaView directly to render high-quality screenshots and animations from the generated VTP and VTI files.
