ACTIVATE=. .venv/bin/activate;
PYTHON=$(ACTIVATE) python
UV=uv
WEBHOOK_URL=

run: 
	$(ACTIVATE) python main.py

install: 
	$(ACTIVATE) $(UV) sync

lint:
	$(ACTIVATE) pycodestyle main.py repositories/ services/
	$(ACTIVATE) mypy main.py repositories/ services/

venv:
	$(UV) venv --python 3.13
