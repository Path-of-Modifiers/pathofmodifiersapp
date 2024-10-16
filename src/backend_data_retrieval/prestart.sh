#! /usr/bin/env bash

python data_retrieval_app/dataretrieval_pre_start.py

# Create initial data in DB
if python data_retrieval_app/data_deposit/main.py; then
    echo "Data deposit successful. Continuing..."
else
    echo "Data deposit failed. Exiting..."
    exit 1
fi

# Test scripts in "tests" module
# python data_retrieval_app/tests/scripts/test_with_sim_data_deposit_pub_stash_data.py

# exit 1

# Variables that need to be set before running container.
# Check if exists or value = changethis
if [[ -z "${POE_PUBLIC_STASHES_AUTH_TOKEN}" ]] || [[ "${POE_PUBLIC_STASHES_AUTH_TOKEN}" == "changethis" ]] ; then
    echo "Env variable POE_PUBLIC_STASHES_AUTH_TOKEN is not set"
    exit 1
fi
if [[ -z "${CURRENT_SOFTCORE_LEAGUE}" ]] || [[ "${CURRENT_SOFTCORE_LEAGUE}" == "changethis" ]]; then
    echo "Env variable CURRENT_SOFTCORE_LEAGUE is not set"
    exit 1
fi
if [[ -z "${OATH_ACC_TOKEN_CONTACT_EMAIL}" ]] || [[ "${OATH_ACC_TOKEN_CONTACT_EMAIL}" == "changethis" ]]; then
    echo "Env variable OATH_ACC_TOKEN_CONTACT_EMAIL is not set"
    exit 1
fi
# Check if MANUAL_NEXT_CHANGE_ID is set, then NEXT_CHANGE_ID have to be set as well
if [[ "${MANUAL_NEXT_CHANGE_ID}" == "True" ]]; then
    if [[ -z "${NEXT_CHANGE_ID}" ]] || [[ "${NEXT_CHANGE_ID}" == "changethis" ]]; then
        echo "Env variable NEXT_CHANGE_ID is not set when MANUAL_NEXT_CHANGE_ID is True"
        exit 1
    fi
fi

while true; do
    python data_retrieval_app/external_data_retrieval/main.py
done
