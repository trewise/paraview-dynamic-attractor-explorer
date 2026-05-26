"""VTK/VTP export utilities using PyVista."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv


def write_point_cloud_vtp(path: str | Path, times: np.ndarray, states: np.ndarray) -> Path:
    """Write attractor states as a ParaView-ready point cloud."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    cloud = pv.PolyData(states)
    cloud["time"] = times
    cloud["point_index"] = np.arange(len(times))
    cloud.save(output)
    return output


def write_trajectory_vtp(path: str | Path, times: np.ndarray, states: np.ndarray) -> Path:
    """Write attractor states as a connected ParaView-ready trajectory polyline."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    poly = pv.PolyData()
    poly.points = states

    n = len(states)
    cells = np.empty(n + 1, dtype=np.int64)
    cells[0] = n
    cells[1:] = np.arange(n)
    poly.lines = cells

    poly["time"] = times
    poly["point_index"] = np.arange(n)
    poly.save(output)
    return output
