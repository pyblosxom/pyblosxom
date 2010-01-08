clean:
	find . -name "*.pyc" -exec 'rm' '{}' ';'

pylint:
	pylint Pyblosxom

test:
	python setup.py test
