.PHONY: serve test typecheck lint lint-fix lint-imports

serve:
	uv run uvicorn python_api.main:app --reload

test:
	uv run pytest

typecheck:
	uv run pyright

install:
	uv sync --no-dev
	@echo "✓ Installation complete"

clean:
	rm -rf .venv && \
	rm -rf __pycache__ && \
	rm -rf .pytest_cache && \
	rm -rf .ruff_cache && \
	find . -type d -name "__pycache__" -exec rm -rf {} + && \
	find . -type f -name "*.pyc" -delete
	@echo "✓ cleaned project"

setup: clean install
	@echo "✓ setup complete"

lint:
	@echo "Verificando problemas no código..."
	uv run ruff check src/

lint-fix:
	@echo "Corrigindo problemas automaticamente..."
	uv run ruff check --fix src/
	@echo "✓ Correções aplicadas"

lint-imports:
	@echo "Organizando imports..."
	uv run ruff check --select I --fix src/
	@echo "✓ Imports organizados"
