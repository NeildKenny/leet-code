#!/usr/bin/env bash

# Basic setup script for Linux Mint
# Installs Python and dependencies, and prepares a virtual environment

set -e

# Update package lists and install Python if needed
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install fastapi==0.110.* sqlalchemy==2.* uvicorn[standard]

echo "Environment setup complete. Activate it with 'source venv/bin/activate'."
