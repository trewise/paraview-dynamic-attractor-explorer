from __future__ import annotations

import sys
from pathlib import Path

from paraview.simple import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from camera_paths.orbit import orbit_position
from camera_paths.flythrough import flythrough_position
from camera_paths.spiral import spiral_position


CAMERAS = {
    "orbit": orbit_position,
    "flythrough": flythrough_position,
    "spiral": spiral_position,
}


dataset = Path(sys.argv[1])
output = Path(sys.argv[2])
camera_name = sys.argv[3]
frame = int(sys.argv[4])
total = int(sys.argv[5])

output.parent.mkdir(parents=True, exist_ok=True)

ResetSession()

reader = XMLPolyDataReader(FileName=[str(dataset)])

view = GetActiveViewOrCreate("RenderView")

tube = Tube(Input=reader)
tube.Radius = 0.08
tube.NumberofSides = 16

display = Show(tube, view)

ColorBy(display, ("POINTS", "time"))
display.RescaleTransferFunctionToDataRange(True, False)

view.Background = [0.02, 0.025, 0.035]
view.ViewSize = [1200, 800]

ResetCamera()

camera = view.GetActiveCamera()

x, y, z = CAMERAS[camera_name](frame, total)

camera.SetPosition(x, y, z)
camera.SetFocalPoint(0, 0, 20)
camera.SetViewUp(0, 0, 1)

Render()

SaveScreenshot(
    str(output),
    view,
    ImageResolution=[1200, 800]
)
