"""ParaView script: render a single trajectory VTP.

Usage with pvpython from the repository root:

pvpython paraview/python_scripts/render_single_attractor.py datasets/attractors/lorenz/lorenz_trajectory.vtp outputs/screenshots/lorenz_trajectory.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from paraview.simple import *


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("datasets/attractors/lorenz/lorenz_trajectory.vtp")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("outputs/screenshots/trajectory_render.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ResetSession()

    reader = XMLPolyDataReader(FileName=[str(input_path)])
    view = GetActiveViewOrCreate("RenderView")

    display = Show(reader, view)
    display.Representation = "Surface"
    display.LineWidth = 2.0

    tube = Tube(Input=reader)
    tube.Radius = 0.08
    tube.NumberofSides = 16
    tube_display = Show(tube, view)
    tube_display.Representation = "Surface"

    ColorBy(tube_display, ("POINTS", "time"))
    tube_display.RescaleTransferFunctionToDataRange(True, False)

    view.Background = [0.02, 0.025, 0.035]
    view.ViewSize = [1600, 1000]

    ResetCamera()
    Render()
    SaveScreenshot(str(output_path), view, ImageResolution=[1600, 1000])


if __name__ == "__main__":
    main()
