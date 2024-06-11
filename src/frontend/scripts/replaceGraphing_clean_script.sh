#!/bin/bash

# Define paths
source_dir="D:/Proggeprosjekter/POE/pathofmodifiersapp/src/frontend/src/hooks/graphing"
destination_dir="D:/Proggeprosjekter/POE/hidden_content/graphing"

# Copy files from source to destination
cp -r "$source_dir"/* "$destination_dir"/
