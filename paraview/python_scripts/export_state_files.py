from __future__ import annotations

import sys
from pathlib import Path

from paraview.simple import *

dataset_root = Path(sys.argv[1])
state_root = Path(sys.argv[2])

state_root.mkdir(parents=True, exist_ok=True)

for attractor_dir in sorted(dataset_root.iterdir()):
    if not attractor_dir.is_dir():
        continue

    name = attractor_dir.name
    trajectory = attractor_dir / f"{name}_trajectory.vtp"
    density = attractor_dir / f"{name}_density.vti"

    if not trajectory.exists():
        print(f"Skipping {name}: missing trajectory")
        continue

    print(f"Exporting trajectory state for {name}")
    ResetSession()

    reader = XMLPolyDataReader(FileName=[str(trajectory)])
    view = GetActiveViewOrCreate("RenderView")

    tube = Tube(Input=reader)
    tube.Radius = 0.08
    tube.NumberofSides = 16

    display = Show(tube, view)
    ColorBy(display, ("POINTS", "time"))
    display.RescaleTransferFunctionToDataRange(True, False)

    view.Background = [0.02, 0.025, 0.035]
    view.ViewSize = [1600, 1000]

    ResetCamera()
    SaveState(str(state_root / f"{name}_trajectory_workflow.pvsm"))

    if density.exists():
        print(f"Exporting density state for {name}")
        ResetSession()

        volume_reader = XMLImageDataReader(FileName=[str(density)])
        volume_view = GetActiveViewOrCreate("RenderView")

        volume_display = Show(volume_reader, volume_view)
        volume_display.Representation = "Volume"
        ColorBy(volume_display, ("POINTS", "density"))

        volume_view.Background = [0.02, 0.025, 0.035]
        volume_view.ViewSize = [1600, 1000]

        ResetCamera()
        SaveState(str(state_root / f"{name}_density_workflow.pvsm"))

print("State export complete.")
