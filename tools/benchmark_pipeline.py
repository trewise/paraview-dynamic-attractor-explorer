"""Simple generation benchmark for the attractor pipeline."""

from __future__ import annotations

import time

from src.attractors import list_systems
from src.generators import generate_attractor_dataset


def main() -> None:
    start = time.perf_counter()
    systems = list_systems()

    for name in systems:
        system_start = time.perf_counter()
        generate_attractor_dataset(name)
        elapsed = time.perf_counter() - system_start
        print(f"{name}: {elapsed:.3f} seconds")

    total = time.perf_counter() - start
    print(f"Generated {len(systems)} systems in {total:.3f} seconds.")


if __name__ == "__main__":
    main()
