# Multi-stage Dockerfile for Catala rules engine
#
# Stages:
#   base    - System dependencies and Catala compiler
#   dev     - Development environment with all tools
#   release - Production-ready image

FROM ocaml/opam:debian-12-ocaml-5.2 AS catala-builder

# Install Catala compiler from opam
RUN opam install catala

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
    && rm -fr /var/lib/apt/lists/*

# Copy Catala compiler from builder stage
COPY --from=catala-builder /home/opam/.opam/default/bin/catala /usr/local/bin/catala
COPY --from=catala-builder /home/opam/.opam/default/lib/catala_runtime_ocaml /usr/local/lib/catala_runtime_ocaml

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

COPY . /app

ENV HOST=0.0.0.0

CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

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

# Compile Catala sources to Python
RUN catala python --plugin-dir /usr/local/lib/catala_runtime_ocaml \
    -o src/generated/example_benefit.py \
    catala/example_benefit.catala_en || true

ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0

USER ${RUN_USER}

CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
