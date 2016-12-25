AWS=$(shell which aws)
package_file_name=aws_billing.zip
function_name=aws_billing
iam_role=

lambda/create: package
	$(AWS) lambda create-function \
		--function-name $(function_name) \
		--runtime "python2.7" \
		--role $(iam_role) \
		--handler aws_billing.handler \
		--zip-file "fileb://$(package_file_name)"

lambda/update: package
	$(AWS) lambda update-function-code \
		--function-name $(function_name) \
		--zip-file "fileb://$(package_file_name)"

package: dist
	cp billing.py $</billing.py
	cp -r lib/python2.7/site-packages/* $</
	cd $< && zip -r ${package_file_name} ./*
	mv -f $</$(package_file_name) ./$(package_file_name)

clean:
	rm -rf dist
	rm -f $(package_file_name)

dist:
	mkdir -p $@

bin/pip:
	$(MAKE) virtualenv

install: bin/pip
	$< install -r requirements.txt

virtualenv:
	virtualenv -p python2 .
