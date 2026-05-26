"""Density volume export utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv


def _expanded_bounds(states: np.ndarray, padding_fraction: float = 0.08) -> tuple[np.ndarray, np.ndarray]:
    mins = states.min(axis=0)
    maxs = states.max(axis=0)
    span = np.maximum(maxs - mins, 1e-6)
    padding = span * padding_fraction
    return mins - padding, maxs + padding


def make_density_volume(
    states: np.ndarray,
    resolution: int = 64,
) -> tuple[pv.ImageData, dict[str, list[float] | int]]:
    """Convert trajectory points into a structured density volume."""
    if resolution < 8:
        raise ValueError("resolution must be at least 8.")

    mins, maxs = _expanded_bounds(states)
    hist, edges = np.histogramdd(
        states,
        bins=(resolution, resolution, resolution),
        range=[
            [mins[0], maxs[0]],
            [mins[1], maxs[1]],
            [mins[2], maxs[2]],
        ],
    )

    spacing = tuple((maxs - mins) / resolution)
    grid = pv.ImageData()
    grid.dimensions = (resolution + 1, resolution + 1, resolution + 1)
    grid.origin = tuple(mins)
    grid.spacing = spacing

    point_density = np.zeros((resolution + 1, resolution + 1, resolution + 1), dtype=float)
    point_density[:-1, :-1, :-1] = hist
    point_density = point_density / max(float(point_density.max()), 1.0)

    grid.point_data["density"] = point_density.ravel(order="F")

    metadata = {
        "resolution": resolution,
        "origin": [float(v) for v in mins],
        "max_bounds": [float(v) for v in maxs],
        "spacing": [float(v) for v in spacing],
        "max_density": float(hist.max()),
    }

    return grid, metadata


def write_density_vti(
    path: str | Path,
    states: np.ndarray,
    resolution: int = 64,
) -> tuple[Path, dict[str, list[float] | int]]:
    """Write trajectory density as ParaView-ready VTI volume."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    grid, metadata = make_density_volume(states, resolution=resolution)
    grid.save(output)
    return output, metadata
