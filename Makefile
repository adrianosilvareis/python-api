.PHONY: serve test typecheck

serve:
	uv run uvicorn src.python_api.main:app --reload

test:
	uv run pytest

typecheck:
	uv run pyright

install:
	uv sync --no-dev
	@echo "✓ Installation complete"

clean:
	rm -rf .venv && rm -rf __pycache__ && find . -type d -name "__pycache__" -exec rm -rf {} + && find . -type f -name "*.pyc" -delete
	@echo "✓ cleaned project"

setup: clean install
	@echo "✓ setup complete"
