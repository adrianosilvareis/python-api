.PHONY: serve test typecheck

serve:
	uv run uvicorn src.python_api.main:app --reload

test:
	uv run pytest

typecheck:
	uv run pyright
