"""Simple generation benchmark for the attractor pipeline."""

from __future__ import annotations

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.attractors import list_systems
from src.generators import generate_attractor_dataset


def main() -> None:
    start = time.perf_counter()
    systems = list_systems()

    for name in systems:
        system_start = time.perf_counter()
        generate_attractor_dataset(name, density_resolution=32)
        elapsed = time.perf_counter() - system_start
        print(f"{name}: {elapsed:.3f} seconds")

    total = time.perf_counter() - start
    print(f"Generated {len(systems)} systems in {total:.3f} seconds.")


if __name__ == "__main__":
    main()
