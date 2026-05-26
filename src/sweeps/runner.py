"""Run parameter sweeps and write sweep metadata."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from src.generators import generate_attractor_dataset
from src.sweeps.configs import SweepConfig, get_sweep


def _safe_float_label(value: float) -> str:
    """Convert a float into a filesystem-safe label."""
    return str(value).replace("-", "neg").replace(".", "p")


def run_sweep(
    sweep: str | SweepConfig,
    output_root: str | Path = "datasets/sweeps",
    metadata_root: str | Path = "metadata/sweeps",
) -> Path:
    """Run a full parameter sweep and write a YAML summary."""
    config = get_sweep(sweep) if isinstance(sweep, str) else sweep
    output_root = Path(output_root)
    metadata_root = Path(metadata_root)
    metadata_root.mkdir(parents=True, exist_ok=True)

    entries = []
    for value in config.values:
        label = _safe_float_label(value)
        output_name = f"{config.system_name}_{config.parameter_name}_{label}"
        outputs = generate_attractor_dataset(
            config.system_name,
            output_root=output_root / config.name,
            t_final=config.t_final,
            dt=config.dt,
            density_resolution=config.density_resolution,
            include_density=True,
            parameter_overrides={config.parameter_name: value},
            output_name=output_name,
        )

        metadata_path = outputs["metadata"]
        metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))

        entries.append(
            {
                "dataset_name": output_name,
                "system_name": config.system_name,
                "parameter_name": config.parameter_name,
                "parameter_value": float(value),
                "files": {key: str(path) for key, path in outputs.items()},
                "bounds": metadata["bounds"],
                "time": metadata["time"],
            }
        )

    summary = {
        "name": config.name,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "system_name": config.system_name,
        "parameter_name": config.parameter_name,
        "values": [float(v) for v in config.values],
        "dataset_count": len(entries),
        "t_final": float(config.t_final),
        "dt": float(config.dt),
        "density_resolution": int(config.density_resolution),
        "datasets": entries,
    }

    summary_path = metadata_root / f"{config.name}_sweep.yaml"
    summary_path.write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8")
    return summary_path
