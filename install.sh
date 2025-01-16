#!/bin/bash

set -e

REPO_URL="https://github.com/Ram001-code/pyHashCat.git"
CLONE_DIR="pyHashCat"  # Directory to clone into

echo "Updating package lists and upgrading installed packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing Hashcat..."
sudo apt install -y hashcat

echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip git

if [ ! -d "$CLONE_DIR" ]; then
    echo "Cloning repository from $REPO_URL..."
    git clone "$REPO_URL" "$CLONE_DIR"
else
    echo "Repository already cloned. Pulling latest changes..."
    cd "$CLONE_DIR"
    git pull
    cd ..
fi

if [ -f "$CLONE_DIR/pyHashCat.py" ]; then
    echo "Setting execute permission on $CLONE_DIR/pyHashCat.py..."
    chmod +x "$CLONE_DIR/pyHashCat.py"
else
    echo "[!] Python script not found in the repository."
fi

echo "Installation complete."
echo "Navigate to the repository directory and run the script. For example:"
echo "  cd $CLONE_DIR"
echo "  ./pyHashCat.py --hashfile <path-to-hashes> --wordlist <path-to-wordlist> [--csv optional_prefix]"
