AWS=$(shell which aws)
PYTHON_RUNTIME=python3.8
package_file_name=aws_billing.zip
function_name=aws-billing
iam_role=
WEBHOOK_URL=

lambda/create: package
	$(AWS) lambda create-function \
		--function-name $(function_name) \
		--runtime "$(PYTHON_RUNTIME)" \
		--role $(iam_role) \
		--handler aws_billing.handler \
		--zip-file "fileb://$(package_file_name)"

lambda/update: package
	$(AWS) lambda update-function-code \
		--function-name $(function_name) \
		--zip-file "fileb://$(package_file_name)"

package: dist
	cp billing.py $</billing.py
	cp -r lib/python3.8/site-packages/* $</
	cd $< && zip -r ${package_file_name} ./*
	mv -f $</$(package_file_name) ./$(package_file_name)

clean:
	rm -rf dist
	rm -f $(package_file_name)

dist:
	mkdir -p $@

run/local: bin/python
	SLACK_WEBHOOK_URL=$(WEBHOOK_URL) $< billing.py

bin/pip:
	$(MAKE) virtualenv

install: bin/pip
	$< install -r requirements.txt

virtualenv:
	virtualenv -p python3 .
