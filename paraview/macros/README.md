# ParaView Macros

This folder stores reusable ParaView macro ideas and helper snippets.

The generated Python scripts in `paraview/python_scripts/` can be run with `pvpython` from the repository root after ParaView is installed.

Example:

```bash
pvpython paraview/python_scripts/render_single_attractor.py datasets/attractors/lorenz/lorenz_trajectory.vtp outputs/screenshots/lorenz_trajectory.png
