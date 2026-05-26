"""Generate ParaView Python scripts for manual or pvpython execution."""

from __future__ import annotations

from pathlib import Path


def write_paraview_scripts(output_dir: str | Path = "paraview/python_scripts") -> list[Path]:
    """Write ParaView automation scripts."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scripts: dict[str, str] = {
        "render_single_attractor.py": SINGLE_ATTRACTOR_SCRIPT,
        "render_density_volume.py": DENSITY_VOLUME_SCRIPT,
        "render_comparison.py": COMPARISON_SCRIPT,
        "orbit_animation_template.py": ORBIT_ANIMATION_SCRIPT,
    }

    written = []
    for filename, content in scripts.items():
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        written.append(path)

    return written


SINGLE_ATTRACTOR_SCRIPT = r'''"""ParaView script: render a single trajectory VTP.

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
'''


DENSITY_VOLUME_SCRIPT = r'''"""ParaView script: render a density VTI volume.

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
'''


COMPARISON_SCRIPT = r'''"""ParaView script: render all-attractor comparison point cloud.

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
'''


ORBIT_ANIMATION_SCRIPT = r'''"""ParaView script template: orbit animation for a trajectory.

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
'''
