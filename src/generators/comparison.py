"""Build multi-attractor comparison datasets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyvista as pv
import yaml


def build_comparison_point_cloud(
    dataset_root: str | Path = "datasets/attractors",
    output_dir: str | Path = "datasets/comparisons",
    output_name: str = "all_attractors_comparison",
    stride: int = 10,
) -> dict[str, Path]:
    """Combine generated attractor point clouds into one labeled comparison file."""
    dataset_root = Path(dataset_root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    points_parts: list[np.ndarray] = []
    attractor_ids: list[np.ndarray] = []
    local_indices: list[np.ndarray] = []
    names: list[str] = []
    table_rows: list[pd.DataFrame] = []

    metadata_paths = sorted(dataset_root.glob("*/*_metadata.json"))
    if not metadata_paths:
        raise FileNotFoundError("No metadata files found. Generate attractor datasets first.")

    for attractor_id, metadata_path in enumerate(metadata_paths):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        name = metadata["name"]
        names.append(name)

        csv_path = Path(metadata["files"]["csv"])
        df = pd.read_csv(csv_path).iloc[::stride].copy()
        points = df[["x", "y", "z"]].to_numpy(dtype=float)

        points_parts.append(points)
        attractor_ids.append(np.full(len(points), attractor_id, dtype=int))
        local_indices.append(np.arange(len(points), dtype=int))

        df["attractor"] = name
        df["attractor_id"] = attractor_id
        table_rows.append(df)

    combined_points = np.vstack(points_parts)
    combined_ids = np.concatenate(attractor_ids)
    combined_local_indices = np.concatenate(local_indices)

    cloud = pv.PolyData(combined_points)
    cloud["attractor_id"] = combined_ids
    cloud["local_index"] = combined_local_indices

    vtp_path = output_dir / f"{output_name}.vtp"
    csv_path = output_dir / f"{output_name}.csv"
    metadata_path = output_dir / f"{output_name}_metadata.yaml"

    cloud.save(vtp_path)
    pd.concat(table_rows, ignore_index=True).to_csv(csv_path, index=False)

    metadata = {
        "name": output_name,
        "dataset_count": len(names),
        "attractors": [{"id": i, "name": name} for i, name in enumerate(names)],
        "stride": stride,
        "files": {
            "comparison_vtp": str(vtp_path),
            "comparison_csv": str(csv_path),
        },
        "paraview_notes": [
            "Open the comparison VTP in ParaView.",
            "Color by attractor_id.",
            "Use Glyph or Point Gaussian representation for a multi-system overview.",
        ],
    }
    metadata_path.write_text(yaml.safe_dump(metadata, sort_keys=False), encoding="utf-8")

    return {
        "comparison_vtp": vtp_path,
        "comparison_csv": csv_path,
        "metadata": metadata_path,
    }
