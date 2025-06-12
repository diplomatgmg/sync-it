FROM python:3.13.4-alpine AS base
FROM base AS builder

ARG SERVICE_PATH=/app/services/parser-service

WORKDIR $SERVICE_PATH

ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=$SERVICE_PATH/src

RUN apk update \
    && apk add --no-cache uv \
    && rm -rf /var/cache/apk/*


# ============================ #
#         DEPS INSTALLING      #
# ============================ #
FROM deps-base AS deps-dev

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen --no-install-project


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM builder AS development

COPY ./src ./src

CMD ["uv", "run", "src/main.py"]
