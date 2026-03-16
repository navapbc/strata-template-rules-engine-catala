# Multi-stage Dockerfile for Catala rules engine
#
# Stages:
#   dev     - Development environment with all tools
#   release - Production-ready image

# -------------------
# Base Python image
# -------------------
FROM python:3.13-slim AS base

RUN pip install --no-cache-dir poetry==1.5

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

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project false && poetry env use python
RUN poetry install --no-root --with dev

ENV HOST=0.0.0.0

# Add project's virtual env to the PATH so we can directly run scripts defined in pyproject.toml
ENV PATH="/app/.venv/bin:$PATH"

CMD ["start-server"]

# ---------
# Release
# ---------
FROM base AS release
ARG RUN_USER

WORKDIR /app
COPY . /app

RUN rm -fr /app/.venv

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install production dependencies only
RUN poetry install --no-root --only main

# Add project's virtual env to the PATH so we can directly run scripts defined in pyproject.toml
ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0

USER ${RUN_USER}

CMD ["start-server"]
