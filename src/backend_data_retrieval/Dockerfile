FROM python:3.11

WORKDIR /data_retrieval_app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# ^^^
# Make sure to update it!

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /data_retrieval_app/


# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/data_retrieval_app

COPY ./prestart.sh /data_retrieval_app/

COPY ./data_retrieval_app /data_retrieval_app/data_retrieval_app
