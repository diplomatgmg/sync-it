FROM python:3.13.4-alpine AS base
FROM base AS builder

ARG APP_PATH=/app
ARG SERVICE_NAME=telegram-api
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
COPY ./libs/common/logger/pyproject.toml ./libs/common/logger/pyproject.toml
COPY ./libs/common/environment/pyproject.toml ./libs/common/environment/pyproject.toml
COPY ./libs/common/gateway/pyproject.toml ./libs/common/gateway/pyproject.toml

FROM deps-base AS deps-dev

RUN uv sync --frozen --dev --package $SERVICE_NAME
RUN uv pip install --no-cache \
    -e /app/libs/common/logger \
    -e /app/libs/common/environment \
    -e /app/libs/common/gateway

FROM deps-base AS deps-prod

RUN uv sync --frozen --no-dev --package $SERVICE_NAME
RUN uv pip install --no-cache \
    -e /app/libs/common/logger \
    -e /app/libs/common/environment \
    -e /app/libs/common/gateway


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM deps-dev AS development

COPY ${SERVICE_PATH}/src ${SERVICE_PATH}/src
COPY ./libs/common/logger ./libs/common/logger
COPY ./libs/common/environment ./libs/common/environment
COPY ./libs/common/gateway ./libs/common/gateway

WORKDIR ${APP_PATH}/${SERVICE_PATH}/src

CMD ["python", "main.py"]
