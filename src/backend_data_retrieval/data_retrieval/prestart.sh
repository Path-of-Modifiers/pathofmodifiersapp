#!/bin/bash

python dataretrieval_pre_start.py

# Create initial data in DB
python modifier_data_deposit/deposit_modifier_data.py



while true
do
 python external_data_retrieval/main.py || echo "App crashed... restarting..." >&2
 echo "Press Ctrl-C to quit." && sleep 1
done
