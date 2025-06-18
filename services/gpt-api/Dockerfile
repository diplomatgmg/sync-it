FROM python:3.13.4-alpine AS base
FROM base AS builder

ARG APP_PATH=/app
ARG SERVICE_PATH=services/gpt-api

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=${APP_PATH} \
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
COPY ./libs/environment ./libs/environment

WORKDIR ${APP_PATH}/${SERVICE_PATH}/src

CMD ["python", "main.py"]
