"""Generate portfolio preview images and GIFs without ParaView."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rendering import render_all_previews, render_orbit_gif, render_sweep_contact_sheet


def main() -> None:
    print("Generating static attractor previews...")
    previews = render_all_previews()
    for path in previews:
        print(f"  preview: {path}")

    print("Generating sweep contact sheets...")
    sweep_outputs = []
    for sweep_path in sorted(Path("metadata/sweeps").glob("*_sweep.yaml")):
        output = Path("outputs/galleries") / f"{sweep_path.stem.replace('_sweep', '')}_contact_sheet.png"
        sweep_outputs.append(render_sweep_contact_sheet(sweep_path, output))
        print(f"  contact sheet: {output}")

    print("Generating orbit GIF previews...")
    gif_targets = [
        ("lorenz", "datasets/attractors/lorenz/lorenz_trajectory.csv"),
        ("rossler", "datasets/attractors/rossler/rossler_trajectory.csv"),
        ("thomas", "datasets/attractors/thomas/thomas_trajectory.csv"),
    ]

    gifs = []
    for name, csv_path in gif_targets:
        output = Path("outputs/animations") / f"{name}_orbit_preview.gif"
        gifs.append(render_orbit_gif(csv_path, output, title=f"{name.title()} Orbit Preview"))
        print(f"  gif: {output}")

    print("Copying selected assets into assets/ and portfolio/ folders...")
    Path("assets/images").mkdir(parents=True, exist_ok=True)
    Path("assets/gifs").mkdir(parents=True, exist_ok=True)
    Path("portfolio/screenshots").mkdir(parents=True, exist_ok=True)
    Path("portfolio/videos").mkdir(parents=True, exist_ok=True)
    Path("docs/screenshots").mkdir(parents=True, exist_ok=True)

    for path in previews:
        shutil.copy2(path, Path("assets/images") / path.name)
        shutil.copy2(path, Path("portfolio/screenshots") / path.name)
        shutil.copy2(path, Path("docs/screenshots") / path.name)

    for path in sweep_outputs:
        shutil.copy2(path, Path("assets/images") / path.name)
        shutil.copy2(path, Path("portfolio/screenshots") / path.name)

    for path in gifs:
        shutil.copy2(path, Path("assets/gifs") / path.name)
        shutil.copy2(path, Path("portfolio/videos") / path.name)

    print("Preview asset generation complete.")


if __name__ == "__main__":
    main()
