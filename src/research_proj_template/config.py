from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = resolve_path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    config.setdefault("project", {})
    config.setdefault("experiment", {})
    config.setdefault("runtime", {})
    config.setdefault("data", {})
    config["_meta"] = {"config_path": str(config_path)}
    return config


def ensure_output_dir(config: dict[str, Any]) -> Path:
    runtime = config.setdefault("runtime", {})
    experiment = config.setdefault("experiment", {})
    output_dir = runtime.get("output_dir", f"artifacts/runs/{experiment.get('name', 'default')}")
    output_path = resolve_path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
