"""Build comparison datasets."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generators import build_comparison_point_cloud


def main() -> None:
    print("Building comparison point cloud...")
    outputs = build_comparison_point_cloud()
    for key, path in outputs.items():
        print(f"  {key}: {path}")
    print("Comparison dataset complete.")


if __name__ == "__main__":
    main()
