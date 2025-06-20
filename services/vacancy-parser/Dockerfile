FROM python:3.13.4-alpine AS base
FROM base AS builder

ARG APP_PATH=/app
ARG SERVICE_NAME=vacancy-parser
ARG SERVICE_PATH=services/$SERVICE_NAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=${APP_PATH}/libs:$APP_PATH/$SERVICE_PATH/src \
    PATH="${APP_PATH}/.venv/bin:$PATH"

WORKDIR ${APP_PATH}

RUN apk update \
    && apk add --no-cache uv \
    && rm -rf /var/cache/apk/*


# ============================ #
#         DEPS INSTALLING      #
# ============================ #
FROM builder AS deps-base

COPY ./pyproject.toml ./uv.lock ./
COPY ${SERVICE_PATH}/pyproject.toml ${SERVICE_PATH}/
COPY ./libs/common/database/pyproject.toml ./libs/common/database/pyproject.toml
COPY ./libs/common/redis/pyproject.toml ./libs/common/redis/pyproject.toml


FROM deps-base AS deps-dev

RUN uv sync --frozen --dev --package $SERVICE_NAME
RUN uv pip install \
    -e /app/libs/common/database \
    -e /app/libs/common/redis

FROM deps-base AS deps-prod

RUN uv sync --frozen --no-dev --package $SERVICE_NAME
RUN uv pip install \
    -e /app/libs/common/database \
    -e /app/libs/common/redis

# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM deps-dev AS development

COPY ${SERVICE_PATH}/src ${SERVICE_PATH}/src
COPY ./libs/common/logger ./libs/common/logger
COPY ./libs/common/redis ./libs/common/redis

WORKDIR ${APP_PATH}/${SERVICE_PATH}/src

CMD ["hupper", "-q", "-m", "main", "-w", "."]
