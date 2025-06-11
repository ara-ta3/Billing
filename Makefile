ACTIVATE=. .venv/bin/activate;
PYTHON=$(ACTIVATE) python
UV=uv

run: 
	SLACK_WEBHOOK_URL=$(WEBHOOK_URL) $(PYTHON) billing.py

install: 
	$(ACTIVATE) $(UV) sync

lint:
	$(ACTIVATE) pycodestyle billing.py
	$(ACTIVATE) mypy billing.py

venv:
	$(UV) venv
