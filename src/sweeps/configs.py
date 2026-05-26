"""Parameter sweep configuration definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SweepConfig:
    """Definition for a one-parameter attractor sweep."""

    name: str
    system_name: str
    parameter_name: str
    values: tuple[float, ...]
    t_final: float
    dt: float
    density_resolution: int = 32


SWEEPS: dict[str, SweepConfig] = {
    "lorenz_rho": SweepConfig(
        name="lorenz_rho",
        system_name="lorenz",
        parameter_name="rho",
        values=(20.0, 24.0, 28.0, 32.0, 36.0, 40.0),
        t_final=35.0,
        dt=0.01,
        density_resolution=32,
    ),
    "rossler_c": SweepConfig(
        name="rossler_c",
        system_name="rossler",
        parameter_name="c",
        values=(3.5, 4.5, 5.7, 7.0, 8.5, 10.0),
        t_final=60.0,
        dt=0.01,
        density_resolution=32,
    ),
    "thomas_b": SweepConfig(
        name="thomas_b",
        system_name="thomas",
        parameter_name="b",
        values=(0.15, 0.18, 0.208186, 0.23, 0.26, 0.30),
        t_final=70.0,
        dt=0.01,
        density_resolution=32,
    ),
}


def list_sweeps() -> list[str]:
    """Return available sweep names."""
    return sorted(SWEEPS)


def get_sweep(name: str) -> SweepConfig:
    """Return one sweep configuration."""
    key = name.lower().strip().replace("-", "_")
    if key not in SWEEPS:
        options = ", ".join(list_sweeps())
        raise KeyError(f"Unknown sweep '{name}'. Available sweeps: {options}")
    return SWEEPS[key]
