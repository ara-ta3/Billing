ACTIVATE=. venv/bin/activate;
PYTHON=$(ACTIVATE) python
PIP=$(ACTIVATE) pip
WEBHOOK_URL=

.PHONY: venv

run/local: 
	SLACK_WEBHOOK_URL=$(WEBHOOK_URL) $(PYTHON) billing.py

install: 
	$(PIP) install -r requirements.txt

lint:
	$(ACTIVATE) pycodestyle billing.py
	$(ACTIVATE) mypy billing.py

freeze:
	$(PIP) freeze > requirements.txt

venv:
	$(PYTHON) -m venv venv
