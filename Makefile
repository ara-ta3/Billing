AWS=aws
PYTHON_RUNTIME=python3.8
ACTIVATE=. venv/bin/activate;
PYTHON=$(ACTIVATE) python
PIP=$(ACTIVATE) pip

package_file_name=aws_billing.zip
function_name=aws-billing
iam_role=
WEBHOOK_URL=

.PHONY: venv

lambda/create: package
	$(AWS) lambda create-function \
		--function-name $(function_name) \
		--runtime "$(PYTHON_RUNTIME)" \
		--role $(iam_role) \
		--handler billing.handler \
		--zip-file "fileb://$(package_file_name)"

lambda/update: package
	$(AWS) lambda update-function-code \
		--function-name $(function_name) \
		--zip-file "fileb://$(package_file_name)"

package: dist
	cp billing.py $</billing.py
	cp -r venv/lib/python3.8/site-packages/* $</
	cd $< && zip -r ${package_file_name} ./*
	mv -f $</$(package_file_name) ./$(package_file_name)

clean:
	rm -rf dist
	rm -f $(package_file_name)
	rm -rf venv

dist:
	mkdir -p $@

run/local: 
	SLACK_WEBHOOK_URL=$(WEBHOOK_URL) $(PYTHON) billing.py

install: 
	$(PIP) install -r requirements.txt

lint:
	$(ACTIVATE) pycodestyle billing.py
	$(ACTIVATE) mypy billing.py

venv:
	python3 -m venv venv
