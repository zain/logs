test:
	nosetests --auto-color tests

test-verbose:
	nosetests --auto-color --nocapture -v tests

travis:
	nosetests -v tests
