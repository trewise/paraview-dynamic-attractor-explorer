# ParaView Dynamic Attractor Explorer

A scientific visualization portfolio project that generates chaotic attractor datasets in Python and renders them with ParaView automation.

This project demonstrates nonlinear simulation, VTK/ParaView-compatible exports, ParaView state-file workflows, scripted visualization filters, screenshots, GIF previews, and MP4 flythrough animations.

---

## Visual Preview

### Multi-Attractor Comparison

![Multi-attractor comparison](portfolio/screenshots/comparison_all_attractors_comparison_paraview.png)

---

## Animation Preview Gallery

The repository includes GIF and MP4 flythrough animations. Static previews are shown below for fast GitHub loading.

### Lorenz Flythrough

![Lorenz preview](portfolio/screenshots/lorenz_preview.png)

[Open Lorenz GIF](portfolio/videos/lorenz_flythrough.gif) | [Open Lorenz MP4](portfolio/videos/lorenz_flythrough.mp4)

### Rossler Flythrough

![Rossler preview](portfolio/screenshots/rossler_preview.png)

[Open Rossler GIF](portfolio/videos/rossler_flythrough.gif) | [Open Rossler MP4](portfolio/videos/rossler_flythrough.mp4)

### Thomas Flythrough

![Thomas preview](portfolio/screenshots/thomas_preview.png)

[Open Thomas GIF](portfolio/videos/thomas_flythrough.gif) | [Open Thomas MP4](portfolio/videos/thomas_flythrough.mp4)

### Aizawa Flythrough

![Aizawa preview](portfolio/screenshots/aizawa_preview.png)

[Open Aizawa GIF](portfolio/videos/aizawa_flythrough.gif) | [Open Aizawa MP4](portfolio/videos/aizawa_flythrough.mp4)

### Chen Flythrough

![Chen preview](portfolio/screenshots/chen_preview.png)

[Open Chen GIF](portfolio/videos/chen_flythrough.gif) | [Open Chen MP4](portfolio/videos/chen_flythrough.mp4)

### Four-Wing Flythrough

![Four-Wing preview](portfolio/screenshots/four_wing_preview.png)

[Open Four-Wing GIF](portfolio/videos/four_wing_flythrough.gif) | [Open Four-Wing MP4](portfolio/videos/four_wing_flythrough.mp4)

---

## Static Screenshot Gallery

### Lorenz Trajectory

![Lorenz preview](portfolio/screenshots/lorenz_preview.png)

### Rossler Trajectory

![Rossler preview](portfolio/screenshots/rossler_preview.png)

### Thomas Trajectory

![Thomas preview](portfolio/screenshots/thomas_preview.png)

### Lorenz Density Volume

![Lorenz density](portfolio/screenshots/density_lorenz_paraview_density.png)

### Rossler Density Volume

![Rossler density](portfolio/screenshots/density_rossler_paraview_density.png)

### Thomas Density Volume

![Thomas density](portfolio/screenshots/density_thomas_paraview_density.png)

---

## Quick Start: Reviewer Path

Run:

    git clone https://github.com/trewise/paraview-dynamic-attractor-explorer.git
    cd paraview-dynamic-attractor-explorer

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    python tools/validate_repository.py
    python tools/project_stats.py
    rm -rf .pytest_cache
    pytest

Expected result:

- repository validation passes
- project statistics print
- tests pass

---

## Quick ParaView Verification

For Ubuntu systems with ParaView Python bindings installed:

    export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

    xvfb-run -a python3 paraview/python_scripts/render_animation.py \
      datasets/attractors/lorenz/lorenz_trajectory.vtp \
      outputs/demo_lorenz_frame.png \
      flythrough \
      0 \
      120

Expected output:

    outputs/demo_lorenz_frame.png

---

## Full Portfolio Render

The full render workflow creates portfolio-scale flythrough frames, GIF previews, and MP4 exports.

    export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
    bash scripts/render/render_missing_flythroughs_safe.sh

Generated media is stored in:

- outputs/animations/
- outputs/flythrough_frames/
- portfolio/videos/
- portfolio/gallery/

---

## Project Highlights

- 11 nonlinear attractor systems
- RK4 numerical integration
- CSV, VTP, VTI, and JSON metadata exports
- ParaView-ready trajectory, point-cloud, and density-volume datasets
- ParaView state files
- ParaView Python scripts and traces
- ParaView macro examples
- Tube, Glyph, Slice, Contour, Threshold, Clip, and Volume Rendering examples
- Color transfer functions
- Parameter sweep visualization
- Multi-attractor comparison animation
- GIF and MP4 animation exports
- Automated validation and project statistics

---

## Repository Structure

    src/                         Core simulation and export code
    scripts/                     Build and rendering automation
    tools/                       Validation and reporting tools
    tests/                       Unit and integration tests
    datasets/attractors/         Generated attractor datasets
    paraview/state_files/        Reusable ParaView state files
    paraview/python_scripts/     ParaView rendering scripts
    paraview/macros/             ParaView macro examples
    outputs/                     Generated images, frames, GIFs, and MP4s
    portfolio/                   Portfolio-ready gallery and report assets
    docs/                        Technical documentation

---

## Documentation

- QUICKSTART.md
- INSTALL.md
- docs/gallery.md
- docs/tutorials/getting_started.md
- docs/tutorials/reproduce_results.md
- docs/workflows/PARAVIEW_WORKFLOW_GUIDE.md
- portfolio/report/final_portfolio_writeup.md

---

## Skills Demonstrated

- Python scientific computing
- Nonlinear dynamical systems
- Numerical ODE simulation
- VTK/ParaView export formats
- ParaView state-file workflows
- ParaView Python automation
- Scientific rendering
- Animation export
- Testing and validation
- Technical documentation

---

## License

MIT License.
