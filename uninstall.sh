#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Variables: ensure this matches the directory created during installation
CLONE_DIR="pyHashCat"

if [ -d "$CLONE_DIR" ]; then
    echo "Removing repository directory '$CLONE_DIR'..."
    rm -rf "$CLONE_DIR"
    echo "Repository directory removed."
else
    echo "[!] Repository directory '$CLONE_DIR' not found."
fi

echo "Uninstallation complete."
