clean:
	find . -name "*.pyc" -exec 'rm' '{}' ';'

pylint:
	pylint Pyblosxom

test:
	nosetests -s --verbose --with-coverage --cover-package=Pyblosxom --include unit
