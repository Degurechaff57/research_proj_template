from __future__ import annotations

import json

from research_proj_template.runner import run_job


def test_run_job_writes_summary(tmp_path):
    output_dir = tmp_path / "artifacts"
    config_path = tmp_path / "smoke.yaml"
    config_path.write_text(
        "\n".join(
            [
                "project:",
                "  name: smoke-project",
                "  stage: test",
                "experiment:",
                "  name: smoke-exp",
                "  description: Smoke test config.",
                "  metric: smoke_metric",
                "runtime:",
                f"  output_dir: {output_dir}",
                "  device: cpu",
                "  seed: 7",
                "data:",
                "  dataset: synthetic",
            ]
        ),
        encoding="utf-8",
    )

    result, summary_path = run_job("demo", config_path)

    assert result["status"] == "ok"
    assert result["project"] == "smoke-project"
    assert result["metric_name"] == "smoke_metric"
    assert summary_path.exists()

    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload["experiment"] == "smoke-exp"
    assert payload["output_dir"] == str(output_dir)
