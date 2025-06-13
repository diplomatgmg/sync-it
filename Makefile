.PHONY: help up upb down stop venv

ыhelp:
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


up: # compose up
	@docker compose up -d

upb: # compose up --build
	@docker compose up -d --build

down: # compose down
	@docker compose down

stop: # compose stop
	@docker compose stop

venv: # create venv
	@uv sync --frozen

lint: # run linters and formatters
	@uv run ruff check . && \
	uv run isort . --check-only && \
	uv run ruff format --check . && \
	uv run mypy .

lint-fix: # run linters and formatters with fix
	@uv run ruff check . && \
	uv run isort . && \
	uv run ruff format . && \
	uv run mypy .

