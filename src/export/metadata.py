"""Metadata export utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from src.attractors.systems import AttractorSystem


def write_metadata(
    path: str | Path,
    system: AttractorSystem,
    times: np.ndarray,
    states: np.ndarray,
    csv_path: str | Path,
    trajectory_vtp_path: str | Path,
    point_cloud_vtp_path: str | Path,
) -> Path:
    """Write dataset metadata as JSON."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "name": system.name,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": system.parameters,
        "initial_state": list(system.initial_state),
        "time": {
            "start": float(times[0]),
            "end": float(times[-1]),
            "steps": int(len(times)),
            "dt": float(times[1] - times[0]) if len(times) > 1 else None,
        },
        "bounds": {
            "x": [float(states[:, 0].min()), float(states[:, 0].max())],
            "y": [float(states[:, 1].min()), float(states[:, 1].max())],
            "z": [float(states[:, 2].min()), float(states[:, 2].max())],
        },
        "files": {
            "csv": str(csv_path),
            "trajectory_vtp": str(trajectory_vtp_path),
            "point_cloud_vtp": str(point_cloud_vtp_path),
        },
        "paraview_notes": [
            "Open the VTP trajectory file in ParaView.",
            "Apply Tube filter to make the curve visible.",
            "Color by time or point index.",
            "Use the point-cloud VTP for glyph-based views.",
        ],
    }

    output.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return output
