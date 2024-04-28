#! /usr/bin/env bash

python dataretrieval_pre_start.py

# Create initial data in DB
python modifier_data_deposit/deposit_modifier_data.py

python external_data_retrieval/main.py