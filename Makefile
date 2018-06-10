SHELL := /bin/bash



.PHONY: dist
dist:
	find . -type f -name "rumps.py" -exec gsed -i '/nsapplication.activateIgnoringOtherApps_\(True\)/d' {} \;
	rm -rf dist build __pycache__
	source dist_env/bin/activate ; \
	python setup.py py2app
