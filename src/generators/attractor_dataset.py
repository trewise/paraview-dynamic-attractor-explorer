"""Generate complete attractor dataset packages."""

from __future__ import annotations

from pathlib import Path

from src.attractors import get_system
from src.export import (
    write_csv,
    write_metadata,
    write_point_cloud_vtp,
    write_trajectory_vtp,
)
from src.solvers import integrate_rk4


def generate_attractor_dataset(
    name: str,
    output_root: str | Path = "datasets/attractors",
    t_final: float | None = None,
    dt: float | None = None,
) -> dict[str, Path]:
    """Generate CSV, VTP, and metadata files for one attractor."""
    system = get_system(name)
    t_final = system.default_t_final if t_final is None else t_final
    dt = system.default_dt if dt is None else dt

    times, states = integrate_rk4(
        derivative=system.derivative,
        initial_state=system.initial_state,
        parameters=system.parameters,
        t_final=t_final,
        dt=dt,
    )

    root = Path(output_root) / system.name
    csv_path = write_csv(root / f"{system.name}_trajectory.csv", times, states)
    trajectory_vtp_path = write_trajectory_vtp(
        root / f"{system.name}_trajectory.vtp", times, states
    )
    point_cloud_vtp_path = write_point_cloud_vtp(
        root / f"{system.name}_point_cloud.vtp", times, states
    )
    metadata_path = write_metadata(
        root / f"{system.name}_metadata.json",
        system,
        times,
        states,
        csv_path,
        trajectory_vtp_path,
        point_cloud_vtp_path,
    )

    return {
        "csv": csv_path,
        "trajectory_vtp": trajectory_vtp_path,
        "point_cloud_vtp": point_cloud_vtp_path,
        "metadata": metadata_path,
    }
