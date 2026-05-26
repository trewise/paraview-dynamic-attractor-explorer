"""Generate all baseline attractor datasets and manifest."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.attractors import list_systems
from src.generators import build_dataset_manifest, generate_attractor_dataset


def main() -> None:
    print("Generating attractor datasets...")
    for name in list_systems():
        print(f"  - {name}")
        outputs = generate_attractor_dataset(name, density_resolution=64)
        for key, path in outputs.items():
            print(f"      {key}: {path}")

    manifest_path = build_dataset_manifest()
    print(f"Dataset manifest: {manifest_path}")
    print("Dataset generation complete.")


if __name__ == "__main__":
    main()
