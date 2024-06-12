#!/bin/bash

# Define relative paths or use environment variables
source_dir="./graphing_decoy"
destination_dir="../src/hooks/graphing"

# Get the absolute path of the current directory
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
	@@ -12,6 +12,4 @@ source_path="$current_dir/$source_dir"
destination_path="$current_dir/$destination_dir"

# Copy files from source to destination
cp -r "$source_path"/* "$destination_path"/

# Gets written to the destination file
echo "DO NOT COMMIT THIS FILE!"