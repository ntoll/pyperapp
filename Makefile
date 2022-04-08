XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)
GREP_T_FLAG := $(shell test $$(uname) = Linux && echo -T)
export PYFLAKES_BUILTINS=_

all:
	@echo "\nThere is no default Makefile target right now. Try:\n"
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make tidy - tidy code with the 'black' formatter."
	@echo "make pyflakes - run the PyFlakes code checker."
	@echo "make pycodestyle - run the PEP8 style checker."
	@echo "make test - run the test suite."
	@echo "make coverage - view a report on test coverage."
	@echo "make check - run all the checkers and tests."
	@echo "make tr_go LANG=xx_XX - create/update a pyperapp.po file for translation."
	@echo "make tr_comp LANG=xx_XX - compile translation strings in pyperapp.po to a pyperapp.mo file."
	@echo "make docs - use Sphinx to create project documentation."
	@echo "make dist- package up PyperApp."
	@echo "make publish-test - upload PyperApp to the test PyPI instance."
	@echo "make publish-live - uplaod PyperApp to the main PyPI instance."

clean:
	rm -rf src/pyperapp.egg-info
	rm -rf .pytest_cache
	rm -rf docs/_build
	rm -rf .eggs
	rm -rf build
	rm -rf dist
	find . \( -name '*.py[co]' -o -name dropin.cache \) -delete
	find . \( -name '*.bak' -o -name dropin.cache \) -delete
	find . \( -name '*.tgz' -o -name dropin.cache \) -delete
	find . \( -name '*.pot' -o -name dropin.cache \) -delete
	find . | grep -E "(__pycache__)" | xargs rm -rf

tidy: clean
	@echo "\nTidying code with black..."
	black -l 79 src
	black -l 79 tests

pyflakes:
	# search the current directory tree for .py files, skipping docs, feeding them to pyflakes
	find . \( -path ./docs -o -name .env \) -type d -prune -o -name '*.py' -print0 | $(XARGS) pyflakes

pycodestyle:
	# search the current directory tree for .py files and feed them to pycodestyle
	find . \( -name .env \) -type d -prune -o -name '*.py' -print0 | $(XARGS) -n 1 pycodestyle --repeat --exclude=docs/*,.vscode/* --ignore=E731,E402,W504,W503

test: clean
	pytest --random-order

coverage: clean
	pytest --random-order --cov-config .coveragerc --cov-report term-missing --cov=src tests/

check: clean tidy pycodestyle pyflakes coverage

tr_go:
	@python utils/translate.py translate_begin LANG=$(LANG)

tr_comp:
	@python utils/translate.py translate_done LANG=$(LANG)

docs: clean
	$(MAKE) -C docs html
	@echo "\nDocumentation can be found here:"
	@echo file://`pwd`/docs/_build/html/index.html
	@echo "\n"

dist: check 
	@echo "\nChecks pass, good to package..."
	python3 -m build

publish-test: dist
	@echo "\nPackaging complete... Uploading to PyPi..."
	python3 -m twine upload --repository testpypi --sign dist/*

publish-live: dist
	@echo "\nPackaging complete... Uploading to PyPi..."
	python3 -m twine upload --sign dist/*
