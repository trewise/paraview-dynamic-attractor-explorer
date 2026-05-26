import json
from pathlib import Path

import yaml

from src.generators.manifest import build_dataset_manifest


def test_manifest_generator_reads_metadata(tmp_path: Path):
    root = tmp_path / "datasets" / "attractors" / "demo"
    root.mkdir(parents=True)

    metadata = {
        "name": "demo",
        "parameters": {"a": 1.0},
        "initial_state": [0.0, 0.0, 0.0],
        "time": {"start": 0.0, "end": 1.0, "steps": 2, "dt": 1.0},
        "bounds": {"x": [0, 1], "y": [0, 1], "z": [0, 1]},
        "files": {
            "csv": "demo.csv",
            "trajectory_vtp": "demo.vtp",
            "point_cloud_vtp": "demo_points.vtp",
            "density_vti": "demo.vti",
        },
        "density_volume": {"resolution": 16},
    }

    (root / "demo_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    output = tmp_path / "manifest.yaml"
    build_dataset_manifest(tmp_path / "datasets" / "attractors", output)

    data = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert data["dataset_count"] == 1
    assert data["datasets"][0]["name"] == "demo"
