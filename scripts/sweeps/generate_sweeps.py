"""Generate all configured parameter sweeps."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sweeps import list_sweeps, run_sweep


def main() -> None:
    print("Generating parameter sweeps...")
    for name in list_sweeps():
        print(f"  - {name}")
        summary_path = run_sweep(name)
        print(f"      summary: {summary_path}")
    print("Parameter sweep generation complete.")


if __name__ == "__main__":
    main()
