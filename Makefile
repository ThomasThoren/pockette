.PHONY: lint precommit test typecheck

precommit: lint typecheck test

lint:
	pylint --reports=no setup.py pockette/ tests/

test:
	pytest --cov-report term-missing --cov=pockette/ tests

typecheck:
	mypy setup.py pockette/ tests/
