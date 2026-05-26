"""Generate lightweight animated GIF previews without requiring ParaView."""

from __future__ import annotations

from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd


def render_orbit_gif(
    csv_path: str | Path,
    output_path: str | Path,
    title: str | None = None,
    stride: int = 8,
    frames: int = 90,
) -> Path:
    """Render a rotating 3D trajectory preview GIF."""
    csv_path = Path(csv_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path).iloc[::stride]
    title = title or csv_path.parent.name.replace("_", " ").title()

    fig = plt.figure(figsize=(7, 6), facecolor="#090d14")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#090d14")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.plot(df["x"], df["y"], df["z"], linewidth=0.45, alpha=0.92)
    ax.set_title(title, color="white", fontsize=16, pad=16)

    def update(frame: int):
        ax.view_init(elev=24, azim=frame * 360 / frames)
        return (ax,)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)
    ani.save(output_path, writer="pillow", fps=20)
    plt.close(fig)
    return output_path
