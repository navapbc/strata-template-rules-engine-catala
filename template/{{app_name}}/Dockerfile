# Multi-stage Dockerfile for Catala rules engine
#
# Stages:
#   dev     - Development environment with all tools
#   release - Production-ready image

# -------------------
# Base Python image
# -------------------
FROM python:3.13-slim AS base

RUN pip install --no-cache-dir uv==0.11.1

RUN apt-get update \
    && apt-get upgrade --yes \
    && apt-get install --no-install-recommends --yes \
    build-essential \
    wget \
    libgmp-dev libmpfr-dev libmpc-dev gcc libc6-dev \
    && rm -fr /var/lib/apt/lists/*

ARG RUN_UID
ARG RUN_USER

RUN : "${RUN_USER:?RUN_USER and RUN_UID need to be set and non-empty.}" && \
    [ "${RUN_USER}" = "root" ] || \
    (useradd --create-home --create --user-group --home "/home/${RUN_USER}" --uid ${RUN_UID} "${RUN_USER}" \
    && mkdir /app \
    && chown -R ${RUN_UID} "/home/${RUN_USER}" /app)

# -----------
# Dev image
# -----------
FROM base AS dev
ARG RUN_USER
USER ${RUN_USER}
WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

RUN uv sync --frozen --extra dev --no-install-project

ENV HOST=0.0.0.0

# Add project's virtual env to the PATH so we can directly run scripts defined in pyproject.toml
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "src.main"]

# ---------
# Release
# ---------
FROM base AS release
ARG RUN_USER

WORKDIR /app
COPY . /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Install production dependencies and project (for console scripts like start-server)
RUN uv sync --frozen --no-dev

# Add project's virtual env to the PATH so we can directly run scripts defined in pyproject.toml
ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0

USER ${RUN_USER}

CMD ["start-server"]
