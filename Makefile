.PHONY: install test lint typecheck e2e clean

install:
	uv pip install -r requirements.txt
	uv pip install -r requirements-dev.txt

test:
	python test_arithmetic_env.py

lint:
	ruff check .

typecheck:
	mypy JAVS_Util Env javs.py test_arithmetic_env.py

e2e:
	python test_e2e.py test_full.ai

ci: lint typecheck test e2e

clean:
	rm -rf build/ dist/ *.egg-info .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +