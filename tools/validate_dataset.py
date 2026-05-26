"""Validate generated attractor dataset outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import pyvista as pv
import yaml


REQUIRED_COLUMNS = {"t", "x", "y", "z", "speed_proxy"}
REQUIRED_FILE_KEYS = {"csv", "trajectory_vtp", "point_cloud_vtp", "density_vti"}


def validate_one(root: Path) -> list[str]:
    errors: list[str] = []

    csv_files = sorted(root.glob("*_trajectory.csv"))
    metadata_files = sorted(root.glob("*_metadata.json"))
    trajectory_files = sorted(root.glob("*_trajectory.vtp"))
    point_cloud_files = sorted(root.glob("*_point_cloud.vtp"))
    density_files = sorted(root.glob("*_density.vti"))

    if not csv_files:
        errors.append(f"{root}: missing trajectory CSV")
    if not metadata_files:
        errors.append(f"{root}: missing metadata JSON")
    if not trajectory_files:
        errors.append(f"{root}: missing trajectory VTP")
    if not point_cloud_files:
        errors.append(f"{root}: missing point-cloud VTP")
    if not density_files:
        errors.append(f"{root}: missing density VTI")

    if csv_files:
        df = pd.read_csv(csv_files[0])
        missing = REQUIRED_COLUMNS.difference(df.columns)
        if missing:
            errors.append(f"{csv_files[0]} missing columns: {sorted(missing)}")
        if len(df) < 100:
            errors.append(f"{csv_files[0]} has too few rows: {len(df)}")
        if df[["x", "y", "z"]].isna().any().any():
            errors.append(f"{csv_files[0]} contains NaN coordinate values")

    if metadata_files:
        data = json.loads(metadata_files[0].read_text(encoding="utf-8"))
        for field in ["name", "parameters", "initial_state", "time", "bounds", "files"]:
            if field not in data:
                errors.append(f"{metadata_files[0]} missing field: {field}")
        file_keys = set(data.get("files", {}))
        missing_file_keys = REQUIRED_FILE_KEYS.difference(file_keys)
        if missing_file_keys:
            errors.append(f"{metadata_files[0]} missing file references: {sorted(missing_file_keys)}")

    if trajectory_files:
        mesh = pv.read(trajectory_files[0])
        if mesh.n_points < 100:
            errors.append(f"{trajectory_files[0]} has too few points: {mesh.n_points}")
        if "time" not in mesh.point_data:
            errors.append(f"{trajectory_files[0]} missing time point data")

    if point_cloud_files:
        mesh = pv.read(point_cloud_files[0])
        if mesh.n_points < 100:
            errors.append(f"{point_cloud_files[0]} has too few points: {mesh.n_points}")
        if "point_index" not in mesh.point_data:
            errors.append(f"{point_cloud_files[0]} missing point_index point data")

    if density_files:
        volume = pv.read(density_files[0])
        if "density" not in volume.point_data:
            errors.append(f"{density_files[0]} missing density point data")
        if volume.n_points < 1000:
            errors.append(f"{density_files[0]} has unexpectedly few grid points: {volume.n_points}")

    return errors


def validate_manifest(dataset_count: int) -> list[str]:
    errors: list[str] = []
    manifest_path = Path("metadata/dataset_manifest.yaml")

    if not manifest_path.exists():
        return ["metadata/dataset_manifest.yaml does not exist"]

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("dataset_count") != dataset_count:
        errors.append(
            f"Manifest dataset_count={manifest.get('dataset_count')} but found {dataset_count}"
        )

    if not manifest.get("paraview_ready"):
        errors.append("Manifest paraview_ready flag is not true")

    if "datasets" not in manifest or len(manifest["datasets"]) != dataset_count:
        errors.append("Manifest datasets list is missing or has incorrect length")

    return errors


def main() -> None:
    dataset_root = Path("datasets/attractors")

    if not dataset_root.exists():
        raise SystemExit("datasets/attractors does not exist. Run scripts/build/generate_all.py first.")

    attractor_dirs = [p for p in sorted(dataset_root.iterdir()) if p.is_dir()]
    if not attractor_dirs:
        raise SystemExit("No attractor datasets found. Run scripts/build/generate_all.py first.")

    errors: list[str] = []
    for root in attractor_dirs:
        errors.extend(validate_one(root))

    errors.extend(validate_manifest(len(attractor_dirs)))

    if errors:
        print("Dataset validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print(f"Dataset validation passed for {len(attractor_dirs)} attractor dataset(s).")


if __name__ == "__main__":
    main()
