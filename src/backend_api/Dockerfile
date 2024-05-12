# Build stage
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 

WORKDIR /app/

ARG POETRY_ENV

ENV POETRY_ENV=${POETRY_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1
# ^^^
# Make sure to update it!

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 


# Copy only the dependencies files
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Project initialization:
RUN POETRY_VIRTUALENVS_CREATE=false poetry install
RUN poetry install --no-interaction

ENV PYTHONPATH=/app

COPY ./app /app/app