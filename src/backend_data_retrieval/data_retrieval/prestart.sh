#! /usr/bin/env bash

python dataretrieval_pre_start.py

# Create initial data in DB
if python modifier_data_deposit/deposit_modifier_data.py; then
    echo "Data modifier deposit successful"
else
    echo "Data modifier deposit failed"
    exit 1
fi

while true; do
    python external_data_retrieval/main.py
done
