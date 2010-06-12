.PHONY: test dist release pypi clean

test:
	py.test -x test

dist: clean test
	python -c 'import spackager; print spackager.__doc__.strip()' > README
	python setup.py sdist

release: dist pypi

pypi: test
	python setup.py sdist upload

clean:
	find . -name "*.pyc" | xargs rm || true
	rm -r dist || true
	rm -r build || true
	rm -r *.egg-info || true
