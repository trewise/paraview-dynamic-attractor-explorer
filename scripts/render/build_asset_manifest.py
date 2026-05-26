"""Build a manifest of generated visual assets."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    image_files = sorted(Path("outputs/screenshots").glob("*.png"))
    gallery_files = sorted(Path("outputs/galleries").glob("*.png"))
    gif_files = sorted(Path("outputs/animations").glob("*.gif"))

    manifest = {
        "title": "Dynamic Attractor Observatory Visual Asset Manifest",
        "static_preview_count": len(image_files),
        "gallery_count": len(gallery_files),
        "gif_count": len(gif_files),
        "static_previews": [str(p) for p in image_files],
        "galleries": [str(p) for p in gallery_files],
        "gifs": [str(p) for p in gif_files],
        "notes": [
            "PNG and GIF previews are generated with matplotlib for portfolio display.",
            "ParaView Python scripts remain available for high-quality scientific rendering.",
            "Final ParaView screenshots should replace or supplement these previews when ParaView rendering is complete.",
        ],
    }

    output = Path("metadata/visual_asset_manifest.yaml")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"Visual asset manifest: {output}")


if __name__ == "__main__":
    main()
