ACTIVATE=. .venv/bin/activate;
PYTHON=$(ACTIVATE) python
UV=uv
WEBHOOK_URL=

run: 
	$(PYTHON) billing.py

install: 
	$(ACTIVATE) $(UV) sync

lint:
	$(ACTIVATE) pycodestyle billing.py
	$(ACTIVATE) mypy billing.py

venv:
	$(UV) venv --python 3.13
