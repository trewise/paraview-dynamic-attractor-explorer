"""Generate static preview images without requiring ParaView."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml


def _set_dark_3d_axis(ax) -> None:
    ax.set_facecolor("#090d14")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False


def render_attractor_preview(
    csv_path: str | Path,
    output_path: str | Path,
    title: str | None = None,
    stride: int = 4,
    dpi: int = 180,
) -> Path:
    """Render a trajectory CSV into a portfolio PNG preview."""
    csv_path = Path(csv_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path).iloc[::stride]
    title = title or csv_path.parent.name.replace("_", " ").title()

    fig = plt.figure(figsize=(9, 7), facecolor="#090d14")
    ax = fig.add_subplot(111, projection="3d")
    _set_dark_3d_axis(ax)

    ax.plot(
        df["x"],
        df["y"],
        df["z"],
        linewidth=0.45,
        alpha=0.92,
    )

    ax.set_title(title, color="white", fontsize=18, pad=18)
    ax.view_init(elev=24, azim=135)

    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return output_path


def render_all_previews(
    dataset_root: str | Path = "datasets/attractors",
    output_dir: str | Path = "outputs/screenshots",
) -> list[Path]:
    """Render one PNG preview for every baseline attractor."""
    dataset_root = Path(dataset_root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    for csv_path in sorted(dataset_root.glob("*/*_trajectory.csv")):
        name = csv_path.parent.name
        output = output_dir / f"{name}_preview.png"
        outputs.append(render_attractor_preview(csv_path, output, title=name.replace("_", " ").title()))

    return outputs


def render_sweep_contact_sheet(
    sweep_metadata_path: str | Path,
    output_path: str | Path,
    stride: int = 8,
    dpi: int = 180,
) -> Path:
    """Render a contact sheet for a parameter sweep."""
    sweep_metadata_path = Path(sweep_metadata_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = yaml.safe_load(sweep_metadata_path.read_text(encoding="utf-8"))
    datasets = data["datasets"]

    cols = 3
    rows = (len(datasets) + cols - 1) // cols

    fig = plt.figure(figsize=(cols * 5.2, rows * 4.6), facecolor="#090d14")

    for i, item in enumerate(datasets, start=1):
        df = pd.read_csv(item["files"]["csv"]).iloc[::stride]
        ax = fig.add_subplot(rows, cols, i, projection="3d")
        _set_dark_3d_axis(ax)
        ax.plot(df["x"], df["y"], df["z"], linewidth=0.38, alpha=0.9)
        value = item["parameter_value"]
        parameter = data["parameter_name"]
        ax.set_title(f"{parameter} = {value:g}", color="white", fontsize=12)
        ax.view_init(elev=24, azim=135)

    fig.suptitle(
        f"{data['system_name'].title()} {data['parameter_name']} Sweep",
        color="white",
        fontsize=22,
        y=0.98,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return output_path
