from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2] if "scripts" in Path(__file__).parts else Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

"""Validate generated attractor dataset outputs."""

import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"t", "x", "y", "z", "speed_proxy"}


def validate_one(root: Path) -> list[str]:
    errors: list[str] = []

    csv_files = sorted(root.glob("*_trajectory.csv"))
    metadata_files = sorted(root.glob("*_metadata.json"))
    trajectory_files = sorted(root.glob("*_trajectory.vtp"))
    point_cloud_files = sorted(root.glob("*_point_cloud.vtp"))

    if not csv_files:
        errors.append(f"{root}: missing trajectory CSV")
    if not metadata_files:
        errors.append(f"{root}: missing metadata JSON")
    if not trajectory_files:
        errors.append(f"{root}: missing trajectory VTP")
    if not point_cloud_files:
        errors.append(f"{root}: missing point-cloud VTP")

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

    if errors:
        print("Dataset validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print(f"Dataset validation passed for {len(attractor_dirs)} attractor dataset(s).")


if __name__ == "__main__":
    main()
