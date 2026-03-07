PYTHON ?= python3
UV ?= uv
CONFIG ?= configs/base.yaml

.PHONY: install install-dev demo train eval benchmark test

install:
	$(UV) pip install -e .

install-dev:
	$(UV) pip install -e ".[dev]"

demo:
	$(PYTHON) scripts/run_demo.py --config $(CONFIG)

train:
	$(PYTHON) scripts/train.py --config configs/exp/main.yaml

eval:
	$(PYTHON) scripts/eval.py --config configs/exp/main.yaml --checkpoint artifacts/checkpoints/best.ckpt

benchmark:
	$(PYTHON) scripts/benchmark.py --config configs/exp/baseline.yaml

test:
	PYTHONPATH=src $(PYTHON) -m pytest
