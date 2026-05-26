# Milestone 02 — Data Generation

## Goal

Create a complete Python pipeline that generates nonlinear attractor datasets for ParaView.

## Systems to Implement

- Lorenz attractor
- Rossler attractor
- Chen attractor
- Aizawa attractor
- Thomas attractor
- Halvorsen attractor
- Dadras attractor
- Four-Wing attractor
- Sprott examples

## Data Products

Each attractor will produce:

- trajectory data
- point-cloud data
- speed or arc-length scalar
- time scalar
- radius scalar
- density volume
- metadata file

## Export Formats

- CSV
- VTP
- VTI
- JSON metadata

## Completion Criteria

- All attractor systems generate successfully.
- All outputs validate successfully.
- Generated files load in ParaView.
- Metadata is saved for every generated dataset.
