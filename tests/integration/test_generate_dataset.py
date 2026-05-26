from pathlib import Path

from src.generators import generate_attractor_dataset


def test_generate_lorenz_dataset(tmp_path: Path):
    outputs = generate_attractor_dataset("lorenz", output_root=tmp_path, t_final=1.0, dt=0.01)

    for path in outputs.values():
        assert path.exists()
        assert path.stat().st_size > 0
