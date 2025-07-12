ACTIVATE=. .venv/bin/activate;
PYTHON=$(ACTIVATE) python
UV=uv
WEBHOOK_URL=

run: 
	$(ACTIVATE) python -m billing.main

install: 
	$(ACTIVATE) $(UV) sync
	$(ACTIVATE) $(UV) pip install -e .

lint:
	$(ACTIVATE) pycodestyle src/
	$(ACTIVATE) mypy src/

venv:
	$(UV) venv --python 3.13
