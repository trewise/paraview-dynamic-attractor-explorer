from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


ROOT = Path.cwd()
portfolio = ROOT / "portfolio" / "screenshots"
galleries = ROOT / "portfolio" / "galleries"
docs_gallery = ROOT / "docs" / "gallery"

portfolio.mkdir(parents=True, exist_ok=True)
galleries.mkdir(parents=True, exist_ok=True)
docs_gallery.mkdir(parents=True, exist_ok=True)


def copy_pngs(source: Path, prefix: str) -> list[Path]:
    copied: list[Path] = []
    if not source.exists():
        return copied

    for path in sorted(source.glob("*.png")):
        target = portfolio / f"{prefix}_{path.name}"
        shutil.copy2(path, target)
        copied.append(target)

    return copied


trajectory = copy_pngs(ROOT / "outputs" / "paraview_screenshots", "trajectory")
density = copy_pngs(ROOT / "outputs" / "paraview_volume_renders", "density")
comparison = copy_pngs(ROOT / "outputs" / "paraview_comparisons", "comparison")


def make_contact_sheet(paths: list[Path], output: Path, title: str, columns: int = 3) -> None:
    if not paths:
        return

    rows = (len(paths) + columns - 1) // columns
    fig = plt.figure(figsize=(columns * 5, rows * 4))
    fig.suptitle(title, fontsize=18)

    for idx, path in enumerate(paths, start=1):
        ax = fig.add_subplot(rows, columns, idx)
        img = mpimg.imread(path)
        ax.imshow(img)
        ax.set_title(path.stem.replace("_", " "), fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    fig.savefig(output, dpi=140)
    plt.close(fig)


make_contact_sheet(
    trajectory,
    galleries / "trajectory_gallery_contact_sheet.png",
    "ParaView Trajectory Gallery",
)

make_contact_sheet(
    density,
    galleries / "density_gallery_contact_sheet.png",
    "ParaView Density Volume Gallery",
)

make_contact_sheet(
    comparison,
    galleries / "comparison_gallery_contact_sheet.png",
    "ParaView Comparison Gallery",
    columns=1,
)

for path in galleries.glob("*.png"):
    shutil.copy2(path, docs_gallery / path.name)

readme = docs_gallery / "README.md"
readme.write_text(
    """# Visualization Gallery

This folder contains generated gallery contact sheets for the ParaView attractor workflows.

## Gallery Assets

- `trajectory_gallery_contact_sheet.png`
- `density_gallery_contact_sheet.png`
- `comparison_gallery_contact_sheet.png`

## Source Asset Types

- ParaView trajectory screenshots
- ParaView density volume renders
- ParaView multi-attractor comparison renders

""",
    encoding="utf-8",
)

print("Copied trajectory screenshots:", len(trajectory))
print("Copied density screenshots:", len(density))
print("Copied comparison screenshots:", len(comparison))
print("Gallery outputs:")
for path in sorted(galleries.glob("*.png")):
    print(path)
