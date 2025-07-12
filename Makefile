UV=uv
WEBHOOK_URL=

run: 
	$(UV) run python -m billing.main

install: 
	$(UV) sync --extra dev
	$(UV) pip install -e .

test:
	$(UV) run --directory . python -m pytest tests/ -v

lint:
	$(UV) run pycodestyle src/
	$(UV) run --directory src mypy --explicit-package-bases .

venv:
	$(UV) venv --python 3.13
