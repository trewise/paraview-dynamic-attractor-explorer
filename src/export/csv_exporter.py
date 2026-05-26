"""CSV exporter for attractor trajectories."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def write_csv(path: str | Path, times: np.ndarray, states: np.ndarray) -> Path:
    """Write trajectory data to CSV."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(
        {
            "t": times,
            "x": states[:, 0],
            "y": states[:, 1],
            "z": states[:, 2],
            "speed_proxy": np.gradient(states[:, 0]) ** 2
            + np.gradient(states[:, 1]) ** 2
            + np.gradient(states[:, 2]) ** 2,
        }
    )
    df.to_csv(output, index=False)
    return output
