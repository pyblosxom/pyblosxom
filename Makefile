clean:
	find . -name "*.pyc" | xargs rm
	find . -name "*~" | xargs rm

pylint:
	pylint Pyblosxom

test:
	python setup.py test
