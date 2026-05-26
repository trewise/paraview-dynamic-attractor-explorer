"""Generate complete attractor dataset packages."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from src.attractors import get_system
from src.export import (
    write_csv,
    write_density_vti,
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
    density_resolution: int = 64,
    include_density: bool = True,
    parameter_overrides: dict[str, float] | None = None,
    output_name: str | None = None,
) -> dict[str, Path]:
    """Generate CSV, VTP, VTI, and metadata files for one attractor."""
    base_system = get_system(name)
    parameters = dict(base_system.parameters)

    if parameter_overrides:
        unknown = set(parameter_overrides).difference(parameters)
        if unknown:
            raise KeyError(
                f"Unknown parameter override(s) for {base_system.name}: {sorted(unknown)}"
            )
        parameters.update(parameter_overrides)

    dataset_name = output_name or base_system.name
    system = replace(base_system, name=dataset_name, parameters=parameters)

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

    density_vti_path = None
    density_metadata = None
    outputs = {
        "csv": csv_path,
        "trajectory_vtp": trajectory_vtp_path,
        "point_cloud_vtp": point_cloud_vtp_path,
    }

    if include_density:
        density_vti_path, density_metadata = write_density_vti(
            root / f"{system.name}_density.vti",
            states,
            resolution=density_resolution,
        )
        outputs["density_vti"] = density_vti_path

    metadata_path = write_metadata(
        root / f"{system.name}_metadata.json",
        system,
        times,
        states,
        csv_path,
        trajectory_vtp_path,
        point_cloud_vtp_path,
        density_vti_path=density_vti_path,
        density_metadata=density_metadata,
    )
    outputs["metadata"] = metadata_path

    return outputs
