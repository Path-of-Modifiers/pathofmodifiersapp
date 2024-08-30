#! /usr/bin/env bash

python dataretrieval_pre_start.py

# Create initial data in DB
if python modifier_data_deposit/deposit_modifier_data.py; then
    echo "Data modifier deposit successful. Continuing..."
else
    echo "Data modifier deposit failed. Exiting..."
    exit 1
fi

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
    python external_data_retrieval/main.py
done
