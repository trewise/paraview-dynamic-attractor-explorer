"""Fourth-order Runge-Kutta solver."""

from __future__ import annotations

from typing import Callable

import numpy as np


Derivative = Callable[[float, np.ndarray, dict[str, float]], np.ndarray]


def integrate_rk4(
    derivative: Derivative,
    initial_state: tuple[float, float, float] | np.ndarray,
    parameters: dict[str, float],
    t_final: float,
    dt: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate a first-order system using fixed-step RK4."""
    if dt <= 0:
        raise ValueError("dt must be positive.")
    if t_final <= 0:
        raise ValueError("t_final must be positive.")

    steps = int(round(t_final / dt)) + 1
    times = np.linspace(0.0, t_final, steps)
    states = np.zeros((steps, 3), dtype=float)
    states[0] = np.asarray(initial_state, dtype=float)

    for i in range(steps - 1):
        t = times[i]
        y = states[i]

        k1 = derivative(t, y, parameters)
        k2 = derivative(t + dt / 2.0, y + dt * k1 / 2.0, parameters)
        k3 = derivative(t + dt / 2.0, y + dt * k2 / 2.0, parameters)
        k4 = derivative(t + dt, y + dt * k3, parameters)

        states[i + 1] = y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        if not np.all(np.isfinite(states[i + 1])):
            raise FloatingPointError(f"Non-finite state encountered at step {i + 1}.")

    return times, states
