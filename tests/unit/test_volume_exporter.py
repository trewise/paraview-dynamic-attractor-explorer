import numpy as np

from src.export.volume_exporter import make_density_volume


def test_density_volume_has_density_array():
    rng = np.random.default_rng(42)
    states = rng.normal(size=(1000, 3))

    grid, metadata = make_density_volume(states, resolution=16)

    assert grid.n_points == 17 * 17 * 17
    assert "density" in grid.point_data
    assert metadata["resolution"] == 16
    assert metadata["max_density"] > 0
