"""Generate all baseline attractor datasets."""

from __future__ import annotations

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
