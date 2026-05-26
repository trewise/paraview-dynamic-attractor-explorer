from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2] if "scripts" in Path(__file__).parts else Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

"""Generate all baseline attractor datasets."""

from src.attractors import list_systems
from src.generators import generate_attractor_dataset


def main() -> None:
    print("Generating baseline attractor datasets...")
    for name in list_systems():
        print(f"  - {name}")
        outputs = generate_attractor_dataset(name)
        for key, path in outputs.items():
            print(f"      {key}: {path}")
    print("Dataset generation complete.")


if __name__ == "__main__":
    main()
