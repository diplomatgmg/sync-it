FROM python:3.13.4-alpine AS base
FROM base AS builder

WORKDIR /app/services/parser-service

ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=/app/src

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
