"""ParaView script: render a density VTI volume.

Usage with pvpython from the repository root:

pvpython paraview/python_scripts/render_density_volume.py datasets/attractors/lorenz/lorenz_density.vti outputs/screenshots/lorenz_density.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from paraview.simple import *


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("datasets/attractors/lorenz/lorenz_density.vti")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("outputs/screenshots/density_render.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ResetSession()

    reader = XMLImageDataReader(FileName=[str(input_path)])
    view = GetActiveViewOrCreate("RenderView")

    display = Show(reader, view)
    display.Representation = "Volume"
    ColorBy(display, ("POINTS", "density"))
    display.RescaleTransferFunctionToDataRange(True, False)

    density_lut = GetColorTransferFunction("density")
    density_lut.ApplyPreset("Viridis (matplotlib)", True)

    density_opacity = GetOpacityTransferFunction("density")
    density_opacity.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 0.85, 0.5, 0.0]

    view.Background = [0.02, 0.025, 0.035]
    view.ViewSize = [1600, 1000]

    ResetCamera()
    Render()
    SaveScreenshot(str(output_path), view, ImageResolution=[1600, 1000])


if __name__ == "__main__":
    main()
