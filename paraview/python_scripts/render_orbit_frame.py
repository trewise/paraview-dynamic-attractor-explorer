from __future__ import annotations

import math
import sys
from pathlib import Path

from paraview.simple import *

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
frame = int(sys.argv[3])
total_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 60

output_path.parent.mkdir(parents=True, exist_ok=True)

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
view.ViewSize = [1200, 800]

ResetCamera()
camera = view.GetActiveCamera()

theta = 2.0 * math.pi * frame / total_frames
camera.SetPosition(85.0 * math.cos(theta), 85.0 * math.sin(theta), 45.0)
camera.SetFocalPoint(0.0, 0.0, 20.0)
camera.SetViewUp(0, 0, 1)

Render()
SaveScreenshot(str(output_path), view, ImageResolution=[1200, 800])
