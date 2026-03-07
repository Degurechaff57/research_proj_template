from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import ensure_output_dir, load_config


DEFAULT_RESULTS = {
    "demo": {"metric_name": "demo_score", "metric_value": 0.50},
    "train": {"metric_name": "validation_score", "metric_value": 0.87},
    "eval": {"metric_name": "evaluation_score", "metric_value": 0.85},
    "benchmark": {"metric_name": "throughput_samples_per_sec", "metric_value": 256.0},
}


def run_job(
    mode: str,
    config_path: str | Path,
    checkpoint: str | None = None,
    profile: bool = False,
) -> tuple[dict[str, Any], Path]:
    config = load_config(config_path)
    output_dir = ensure_output_dir(config)
    template_metrics = DEFAULT_RESULTS.get(mode, DEFAULT_RESULTS["demo"])

    result = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "status": "ok",
        "mode": mode,
        "project": config["project"].get("name", "unknown-project"),
        "stage": config["project"].get("stage", "draft"),
        "experiment": config["experiment"].get("name", "default"),
        "description": config["experiment"].get("description", ""),
        "config_path": config["_meta"]["config_path"],
        "output_dir": str(output_dir),
        "device": config["runtime"].get("device", "cpu"),
        "seed": config["runtime"].get("seed", 42),
        "dataset": config["data"].get("dataset", ""),
        "metric_name": config["experiment"].get("metric", template_metrics["metric_name"]),
        "metric_value": template_metrics["metric_value"],
        "checkpoint": checkpoint,
        "profile_enabled": profile,
    }

    summary_path = output_dir / f"{mode}_summary.json"
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result, summary_path
