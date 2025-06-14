FROM python:${PYTHON_VERSION}-alpine AS base
FROM base AS builder

ARG SERVICE_PATH=services/parser/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=$DOCKER_DOCKER_APP_PATH \
    PATH="$DOCKER_APP_PATH/.venv/bin:$PATH"

WORKDIR $DOCKER_APP_PATH

RUN apk update \
    && apk add --no-cache uv \
    && rm -rf /var/cache/apk/*


# ============================ #
#         DEPS INSTALLING      #
# ============================ #
FROM builder AS deps-base

COPY ./pyproject.toml ./uv.lock ./
COPY ${SERVICE_PATH}/pyproject.toml ${SERVICE_PATH}

FROM deps-base AS deps-dev

RUN uv sync --frozen --dev

FROM deps-base AS deps-prod

RUN uv sync --frozen --no-dev


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM deps-dev AS development

COPY ${SERVICE_PATH}/src ${SERVICE_PATH}/src
COPY ./libs/logger ./libs/logger
COPY ./libs/database ./libs/database

WORKDIR $DOCKER_APP_PATH/${SERVICE_PATH}/src

CMD ["hupper", "-q", "-m", "main"]
