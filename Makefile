help:
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^#@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

up: # compose up
	@docker compose up -d

upb: # compose up --build
	@docker compose up -d --build

down: # compose down
	@docker compose down

stop: # compose stop
	@docker compose stop

venv: # create venv
	@uv sync --frozen --all-packages

add: # add python package to service
	@if [ $(words $(MAKECMDGOALS)) -ne 3 ]; then \
		echo "Usage: make add <package> <service>"; \
		exit 1; \
	fi; \
	uv add $(word 2, $(MAKECMDGOALS)) --package $(word 3, $(MAKECMDGOALS))

#MYPY_DIRS := $(shell find services -type d -name src)
#
#lint: # run linters and formatters
#	@uv run ruff check . && \
#	uv run isort . --check-only && \
#	uv run ruff format --check . && \
#	$(foreach dir, $(MYPY_DIRS), uv run mypy $(dir) &&) true
#
#lint-fix: # run linters and formatters with fix
#	@uv run ruff check . && \
#	uv run isort . && \
#	uv run ruff format . && \
#	$(foreach dir, $(MYPY_DIRS), uv run mypy $(dir) &&) true
#
#mm: # create migration for service
#	@if [ -z "$(s)" ] || [ -z "$(m)" ]; then \
#		echo "Usage: make mm s=<service_name> m=\"migration message\""; \
#		exit 1; \
#	fi; \
#	alembic -n $(s) revision --autogenerate -m "$(m)"
#
#migrate: # apply migrations for service
#	@if [ -z "$(s)" ]; then \
#		echo "Usage: make migrate s=<service_name>"; \
#		exit 1; \
#	fi; \
#	alembic -n $(s) upgrade head

%:
	@: