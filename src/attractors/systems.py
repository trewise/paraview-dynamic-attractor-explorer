"""Chaotic attractor system definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


State = np.ndarray
DerivativeFunction = Callable[[float, State, dict[str, float]], State]


@dataclass(frozen=True)
class AttractorSystem:
    """Container for a continuous-time nonlinear dynamical system."""

    name: str
    derivative: DerivativeFunction
    parameters: dict[str, float]
    initial_state: tuple[float, float, float]
    default_t_final: float = 40.0
    default_dt: float = 0.01


def lorenz(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    sigma = p["sigma"]
    rho = p["rho"]
    beta = p["beta"]
    return np.array(
        [
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z,
        ],
        dtype=float,
    )


def rossler(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    a = p["a"]
    b = p["b"]
    c = p["c"]
    return np.array(
        [
            -y - z,
            x + a * y,
            b + z * (x - c),
        ],
        dtype=float,
    )


def chen(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    a = p["a"]
    b = p["b"]
    c = p["c"]
    return np.array(
        [
            a * (y - x),
            (c - a) * x - x * z + c * y,
            x * y - b * z,
        ],
        dtype=float,
    )


def aizawa(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    a = p["a"]
    b = p["b"]
    c = p["c"]
    d = p["d"]
    e = p["e"]
    f = p["f"]
    return np.array(
        [
            (z - b) * x - d * y,
            d * x + (z - b) * y,
            c + a * z - (z**3) / 3.0 - (x**2 + y**2) * (1.0 + e * z)
            + f * z * x**3,
        ],
        dtype=float,
    )


def thomas(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    b = p["b"]
    return np.array(
        [
            np.sin(y) - b * x,
            np.sin(z) - b * y,
            np.sin(x) - b * z,
        ],
        dtype=float,
    )


SYSTEMS: dict[str, AttractorSystem] = {
    "lorenz": AttractorSystem(
        name="lorenz",
        derivative=lorenz,
        parameters={"sigma": 10.0, "rho": 28.0, "beta": 8.0 / 3.0},
        initial_state=(1.0, 1.0, 1.0),
    ),
    "rossler": AttractorSystem(
        name="rossler",
        derivative=rossler,
        parameters={"a": 0.2, "b": 0.2, "c": 5.7},
        initial_state=(1.0, 0.0, 0.0),
        default_t_final=80.0,
    ),
    "chen": AttractorSystem(
        name="chen",
        derivative=chen,
        parameters={"a": 35.0, "b": 3.0, "c": 28.0},
        initial_state=(-10.0, 0.0, 37.0),
    ),
    "aizawa": AttractorSystem(
        name="aizawa",
        derivative=aizawa,
        parameters={"a": 0.95, "b": 0.7, "c": 0.6, "d": 3.5, "e": 0.25, "f": 0.1},
        initial_state=(0.1, 0.0, 0.0),
        default_t_final=80.0,
    ),
    "thomas": AttractorSystem(
        name="thomas",
        derivative=thomas,
        parameters={"b": 0.208186},
        initial_state=(0.1, 0.0, 0.0),
        default_t_final=100.0,
    ),
}


def list_systems() -> list[str]:
    """Return available attractor names."""
    return sorted(SYSTEMS)


def get_system(name: str) -> AttractorSystem:
    """Fetch an attractor system by name."""
    key = name.lower().strip()
    if key not in SYSTEMS:
        options = ", ".join(list_systems())
        raise KeyError(f"Unknown attractor system '{name}'. Available systems: {options}")
    return SYSTEMS[key]
