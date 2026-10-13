#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python /app/backend_api/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/backend_api/app/initial_data.py

fastapi run --reload "backend_api/app/main.py"
