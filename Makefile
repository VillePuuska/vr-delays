lint:
	uv run ruff check

type-check:
	uv run mypy .

ci: lint type-check
