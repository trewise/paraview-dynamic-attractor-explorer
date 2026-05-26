# ParaView Workflow Guide

## Trajectory Visualization

Inputs

- attractor_trajectory.vtp

Pipeline

Reader
→ Tube
→ Color By Arc Length
→ Render

Outputs

- Trajectory screenshots
- Trajectory state files

---

## Density Visualization

Inputs

- attractor_density.vti

Pipeline

Reader
→ Volume Rendering
→ Opacity Transfer Function
→ Color Transfer Function
→ Render

Outputs

- Density screenshots
- Density state files

---

## Comparison Visualization

Inputs

- Multiple trajectory datasets

Pipeline

Readers
→ Coloring
→ Combined Render

Outputs

- Comparison screenshots
- Comparison gallery

---

## Orbit Animation Workflow

Inputs

- attractor_trajectory.vtp

Pipeline

Reader
→ Orbit Camera
→ Frame Rendering
→ FFmpeg Encoding

Outputs

- MP4 animation
- Preview GIF
- Rendered frame sequence

---

## Reusing State Files

Open ParaView

File → Load State

Select:

- *_trajectory_workflow.pvsm
or
- *_density_workflow.pvsm

Replace file paths when prompted.

The visualization pipeline will be restored automatically.
