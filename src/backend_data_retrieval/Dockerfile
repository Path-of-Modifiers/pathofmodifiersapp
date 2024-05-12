FROM python:3.11

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

WORKDIR /data_retrieval/

# Copy only the dependencies files
COPY ./data_retrieval/pyproject.toml ./data_retrieval/poetry.lock* /data_retrieval/

# Project initialization:
RUN POETRY_VIRTUALENVS_CREATE=false poetry install
RUN poetry install --no-interaction

ENV PYTHONPATH=/data_retrieval


COPY ./data_retrieval /data_retrieval
ENTRYPOINT [ "/data_retrieval/prestart.sh" ]