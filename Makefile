SHELL := /bin/bash


PYTHON_EXE := python3.6
PYTHON_ENV := .tox/py36
PYTHON_BIN := $(PYTHON_ENV)/bin



$(PYTHON_BIN)/activate:
	virtualenv -p $(PYTHON_EXE) $(PYTHON_ENV)


.PHONY: virtualenv
virtualenv: $(PYTHON_BIN)/activate
	$(PYTHON_BIN)/pip install -r requirements.txt
	$(PYTHON_BIN)/pip install py2app


clean-postbuild:
	rm -rf build

clean: clean-postbuild
	rm -rf dist
	rm -rf __pycache__
	rm -rf shotput/__pycache__
	rm -rf .eggs


.PHONY: dist
dist: clean
	find . -type f -name "rumps.py" -exec gsed -i '/nsapplication.activateIgnoringOtherApps_\(True\)/d' {} \;
	source $(PYTHON_BIN)/activate ; \
	python setup.py py2app
	$(MAKE) clean-postbuild
