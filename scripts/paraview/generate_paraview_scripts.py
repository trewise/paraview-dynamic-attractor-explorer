"""Generate ParaView Python automation scripts."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization import write_paraview_scripts


def main() -> None:
    print("Writing ParaView automation scripts...")
    for path in write_paraview_scripts():
        print(f"  - {path}")
    print("ParaView scripts complete.")


if __name__ == "__main__":
    main()
