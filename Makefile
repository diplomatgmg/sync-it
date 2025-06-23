COMPOSE_DIR := infra/docker
COMPOSE_COMMAND := docker compose -f $(COMPOSE_DIR)/docker-compose.yml --env-file infra/.env
SERVICES := gpt-api telegram-api vacancy-parser vacancy-processor
MYPY_DIRS := libs $(foreach service,$(SERVICES),services/$(service)/src)

define compose_action
	@if [ -z "$(s)" ]; then \
		echo $(COMPOSE_COMMAND) --profile "*" $(1) $(e); \
		$(COMPOSE_COMMAND) --profile "*" $(1) $(e); \
	elif echo "$(SERVICES)" | grep -w "$(s)" > /dev/null; then \
		echo $(COMPOSE_COMMAND) --profile $(s) $(1) $(e); \
		$(COMPOSE_COMMAND) --profile $(s) $(1) $(e); \
	else \
		echo "Unknown service: $(s)"; \
		echo "Available services: $(SERVICES)"; \
		exit 1; \
	fi
endef

help:
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^#@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

up: # compose up [s=<service>] [e="<extra> <extra2>"]
	$(call compose_action,up -d)

down: # compose down [s=<service>] [e="<extra> <extra2>"]
	$(call compose_action,down)

stop: # compose stop [s=<service>] [e="<extra> <extra2>"]
	$(call compose_action,stop)

venv: # create venv
	@uv sync --frozen --all-packages

add: # add python package to service
	@if [ -z "$(p)" ] || [ -z "$(s)" ]; then \
		echo "Usage: make add p=<package> s=<service> [dev=1]"; \
		exit 1; \
	fi; \
	if [ "$(dev)" = "1" ]; then \
		uv add $(p) --package $(s) --dev; \
	else \
		uv add $(p) --package $(s); \
	fi

lint: # run linters and formatters
	@uv run ruff check . && \
	uv run isort . --check-only && \
	uv run ruff format --check . && \
	$(foreach dir, $(MYPY_DIRS), uv run mypy $(dir) &&) true

lint-fix: # run linters and formatters with fix
	@uv run ruff check . && \
	uv run isort . && \
	uv run ruff format . && \
	$(foreach dir, $(MYPY_DIRS), uv run mypy $(dir) &&) true

mm: # create migration for service
	@if [ -z "$(s)" ] || [ -z "$(m)" ]; then \
		echo "Usage: make mm s=<service_name> m=\"migration message\""; \
		exit 1; \
	fi;
	$(COMPOSE_COMMAND) exec --workdir /app/services/$(s) $(s) alembic revision --autogenerate -m "$(m)"

migrate: # apply migrations for service
	@if [ -z "$(s)" ]; then \
		echo "Usage: make migrate s=<service_name>"; \
		exit 1; \
	fi;
	$(COMPOSE_COMMAND) exec --workdir /app/services/$(s) $(s) alembic upgrade head
	@echo "Migrations applied for service $(s)"

downgrade: # downgrade migration for service
	@if [ -z "$(s)" ] || [ -z "$(r)" ]; then \
		echo "Usage: make downgrade s=<service_name> r=<revision>"; \
		exit 1; \
	fi; \
	$(COMPOSE_COMMAND) exec --workdir /app/services/$(s) $(s) alembic downgrade $(r)
