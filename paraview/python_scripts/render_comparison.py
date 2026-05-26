"""ParaView script: render all-attractor comparison point cloud.

Usage with pvpython from the repository root:

pvpython paraview/python_scripts/render_comparison.py datasets/comparisons/all_attractors_comparison.vtp outputs/screenshots/all_attractors_comparison.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from paraview.simple import *


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("datasets/comparisons/all_attractors_comparison.vtp")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("outputs/screenshots/all_attractors_comparison.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ResetSession()

    reader = XMLPolyDataReader(FileName=[str(input_path)])
    view = GetActiveViewOrCreate("RenderView")

    display = Show(reader, view)
    display.Representation = "Point Gaussian"
    display.GaussianRadius = 0.08

    ColorBy(display, ("POINTS", "attractor_id"))
    display.RescaleTransferFunctionToDataRange(True, False)

    view.Background = [0.02, 0.025, 0.035]
    view.ViewSize = [1800, 1100]

    ResetCamera()
    Render()
    SaveScreenshot(str(output_path), view, ImageResolution=[1800, 1100])


if __name__ == "__main__":
    main()
