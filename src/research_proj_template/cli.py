from __future__ import annotations

import argparse
import json

from .runner import run_job


def build_parser(mode: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"Run the {mode} pipeline.")
    parser.add_argument("--config", required=True, help="Path to a config file.")
    parser.add_argument(
        "--checkpoint",
        default=None,
        help="Optional checkpoint path, typically used for evaluation.",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable profiling mode for this run.",
    )
    return parser


def main(mode: str) -> int:
    args = build_parser(mode).parse_args()
    result, summary_path = run_job(
        mode=mode,
        config_path=args.config,
        checkpoint=args.checkpoint,
        profile=args.profile,
    )
    print(json.dumps(result, indent=2))
    print(f"Summary written to: {summary_path}")
    return 0
