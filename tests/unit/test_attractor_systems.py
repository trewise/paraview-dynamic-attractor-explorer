import numpy as np
import pytest

from src.attractors import get_system, list_systems


def test_system_registry_has_baseline_systems():
    systems = list_systems()
    assert "lorenz" in systems
    assert "rossler" in systems
    assert "chen" in systems
    assert "halvorsen" in systems
    assert "dadras" in systems
    assert "four_wing" in systems
    assert "sprott_a" in systems


def test_lorenz_derivative_shape():
    system = get_system("lorenz")
    derivative = system.derivative(0.0, np.array(system.initial_state), system.parameters)
    assert derivative.shape == (3,)
    assert np.all(np.isfinite(derivative))


def test_unknown_system_raises_key_error():
    with pytest.raises(KeyError):
        get_system("not-a-system")
