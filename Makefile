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

lint-type:
	$(UV) run mypy --ignore-missing-imports src/

lint-fix:
	$(UV) run autopep8 --in-place --recursive src/

venv:
	$(UV) venv --python 3.13
