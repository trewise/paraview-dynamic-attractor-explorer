import numpy as np

from src.solvers import integrate_rk4


def linear_decay(t, state, parameters):
    return -parameters["k"] * state


def test_rk4_integrates_linear_decay():
    times, states = integrate_rk4(
        derivative=linear_decay,
        initial_state=np.array([1.0, 1.0, 1.0]),
        parameters={"k": 1.0},
        t_final=1.0,
        dt=0.01,
    )

    assert len(times) == len(states)
    assert states.shape[1] == 3
    assert np.allclose(states[-1], np.exp(-1.0), atol=1e-5)
