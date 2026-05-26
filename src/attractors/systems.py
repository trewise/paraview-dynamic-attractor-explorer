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
    return np.array(
        [
            p["sigma"] * (y - x),
            x * (p["rho"] - z) - y,
            x * y - p["beta"] * z,
        ],
        dtype=float,
    )


def rossler(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            -y - z,
            x + p["a"] * y,
            p["b"] + z * (x - p["c"]),
        ],
        dtype=float,
    )


def chen(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            p["a"] * (y - x),
            (p["c"] - p["a"]) * x - x * z + p["c"] * y,
            x * y - p["b"] * z,
        ],
        dtype=float,
    )


def aizawa(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            (z - p["b"]) * x - p["d"] * y,
            p["d"] * x + (z - p["b"]) * y,
            p["c"]
            + p["a"] * z
            - (z**3) / 3.0
            - (x**2 + y**2) * (1.0 + p["e"] * z)
            + p["f"] * z * x**3,
        ],
        dtype=float,
    )


def thomas(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            np.sin(y) - p["b"] * x,
            np.sin(z) - p["b"] * y,
            np.sin(x) - p["b"] * z,
        ],
        dtype=float,
    )


def halvorsen(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    a = p["a"]
    return np.array(
        [
            -a * x - 4.0 * y - 4.0 * z - y**2,
            -a * y - 4.0 * z - 4.0 * x - z**2,
            -a * z - 4.0 * x - 4.0 * y - x**2,
        ],
        dtype=float,
    )


def dadras(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            y - p["a"] * x + p["b"] * y * z,
            p["c"] * y - x * z + z,
            p["d"] * x * y - p["e"] * z,
        ],
        dtype=float,
    )


def four_wing(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array(
        [
            p["a"] * x + y * z,
            p["b"] * x + p["c"] * y - x * z,
            -z - x * y,
        ],
        dtype=float,
    )


def sprott_a(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array([y, -x + y * z, p["a"] - y**2], dtype=float)


def sprott_b(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array([y * z, x - y, p["a"] - x * y], dtype=float)


def sprott_c(_: float, state: State, p: dict[str, float]) -> State:
    x, y, z = state
    return np.array([y * z, x - y, p["a"] - x**2], dtype=float)


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
    "halvorsen": AttractorSystem(
        name="halvorsen",
        derivative=halvorsen,
        parameters={"a": 1.4},
        initial_state=(-1.48, -1.51, 2.04),
        default_t_final=60.0,
    ),
    "dadras": AttractorSystem(
        name="dadras",
        derivative=dadras,
        parameters={"a": 3.0, "b": 2.7, "c": 1.7, "d": 2.0, "e": 9.0},
        initial_state=(1.0, 1.0, 1.0),
        default_t_final=40.0,
    ),
    "four_wing": AttractorSystem(
        name="four_wing",
        derivative=four_wing,
        parameters={"a": 0.2, "b": 0.01, "c": -0.4},
        initial_state=(0.1, 0.0, 0.0),
        default_t_final=120.0,
    ),
    "sprott_a": AttractorSystem(
        name="sprott_a",
        derivative=sprott_a,
        parameters={"a": 1.0},
        initial_state=(0.1, 0.0, 0.0),
        default_t_final=80.0,
    ),
    "sprott_b": AttractorSystem(
        name="sprott_b",
        derivative=sprott_b,
        parameters={"a": 1.0},
        initial_state=(0.1, 0.1, 0.1),
        default_t_final=80.0,
    ),
    "sprott_c": AttractorSystem(
        name="sprott_c",
        derivative=sprott_c,
        parameters={"a": 1.0},
        initial_state=(0.1, 0.1, 0.1),
        default_t_final=80.0,
    ),
}


def list_systems() -> list[str]:
    """Return available attractor names."""
    return sorted(SYSTEMS)


def get_system(name: str) -> AttractorSystem:
    """Fetch an attractor system by name."""
    key = name.lower().strip().replace("-", "_")
    if key not in SYSTEMS:
        options = ", ".join(list_systems())
        raise KeyError(f"Unknown attractor system '{name}'. Available systems: {options}")
    return SYSTEMS[key]
