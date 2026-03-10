# Multi-stage Dockerfile for Catala rules engine
#
# Stages:
#   base    - System dependencies and Catala compiler
#   dev     - Development environment with all tools
#   release - Production-ready image

FROM ocaml/opam:debian-12-ocaml-5.4 AS catala-builder

# Install system dependencies required by Catala's opam packages
RUN sudo apt-get update \
    && sudo apt-get install --no-install-recommends --yes \
    libgmp-dev ninja-build pkg-config \
    && sudo rm -fr /var/lib/apt/lists/*

# Install Catala compiler from opam
RUN opam update && opam install catala.1.1.0

# Copy Catala sources and clerk config, then build
COPY --chown=opam:opam catala/src catala/src
COPY --chown=opam:opam catala/clerk.toml catala/clerk.toml
WORKDIR /home/opam/catala
RUN opam exec -- clerk build
WORKDIR /home/opam

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

CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------
# Release
# ---------
FROM base AS release
ARG RUN_USER

WORKDIR /app
COPY . /app
COPY --from=catala-builder /home/opam/catala/_build/libcatala/python/dates.py /app/src/generated/
COPY --from=catala-builder /home/opam/catala/_target/paidleave/python/  /app/src/generated/

RUN rm -fr /app/.venv

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install production dependencies only
RUN poetry install --no-root --only main


ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0

USER ${RUN_USER}

CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
