FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN useradd -ms /bin/bash admin
WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/app

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./app /app/app

RUN mkdir -p /app/app/logs && chown -R admin:admin /app/app/logs

RUN chown -R admin:admin /app
RUN chmod 755 /app
USER admin
