#!/bin/bash
# Clean up pytest cache and temporary files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name ".pytest_cache" -exec rm -r {} +

# Run pytest, passing any additional arguments (like specific test files) to it
pytest "$@"
