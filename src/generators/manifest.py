"""Build YAML dataset manifests."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


def build_dataset_manifest(
    dataset_root: str | Path = "datasets/attractors",
    output_path: str | Path = "metadata/dataset_manifest.yaml",
) -> Path:
    """Create a manifest summarizing all generated attractor datasets."""
    dataset_root = Path(dataset_root)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for metadata_path in sorted(dataset_root.glob("*/*_metadata.json")):
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        entries.append(
            {
                "name": data["name"],
                "parameters": data["parameters"],
                "initial_state": data["initial_state"],
                "time": data["time"],
                "bounds": data["bounds"],
                "files": data["files"],
                "density_volume": data.get("density_volume", {}),
            }
        )

    manifest = {
        "title": "Dynamic Attractor Observatory Dataset Manifest",
        "dataset_root": str(dataset_root),
        "dataset_count": len(entries),
        "formats": ["csv", "vtp", "vti", "json"],
        "paraview_ready": True,
        "datasets": entries,
    }

    output_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return output_path
