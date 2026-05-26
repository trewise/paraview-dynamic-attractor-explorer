"""ParaView script template: orbit animation for a trajectory.

Usage with pvpython from the repository root:

pvpython paraview/python_scripts/orbit_animation_template.py datasets/attractors/lorenz/lorenz_trajectory.vtp outputs/animations/lorenz_orbit
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from paraview.simple import *


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("datasets/attractors/lorenz/lorenz_trajectory.vtp")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("outputs/animations/lorenz_orbit")
    output_dir.mkdir(parents=True, exist_ok=True)

    ResetSession()

    reader = XMLPolyDataReader(FileName=[str(input_path)])
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
    camera = view.GetActiveCamera()

    center = [0.0, 0.0, 20.0]
    radius = 90.0
    height = 45.0

    for frame in range(120):
        theta = 2.0 * math.pi * frame / 120.0
        camera.SetPosition(
            center[0] + radius * math.cos(theta),
            center[1] + radius * math.sin(theta),
            center[2] + height,
        )
        camera.SetFocalPoint(center)
        camera.SetViewUp(0, 0, 1)
        Render()
        SaveScreenshot(str(output_dir / f"frame_{frame:04d}.png"), view, ImageResolution=[1600, 1000])


if __name__ == "__main__":
    main()
