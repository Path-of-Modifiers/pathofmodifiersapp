#!/bin/bash

# Define relative paths or use environment variables
source_dir="./graphing"
destination_dir="../src/hooks/graphing"

# Get the absolute path of the current directory
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Construct absolute paths
source_path="$current_dir/$source_dir"
destination_path="$current_dir/$destination_dir"

# Copy files from source to destination
cp -r "$source_path"/* "$destination_path"/

echo "Frontend graphing hooks replaced with clean version."
