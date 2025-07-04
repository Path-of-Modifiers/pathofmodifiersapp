#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py

fastapi run --reload "app/main.py"
