#!/usr/bin/env bash

# Start the DnD Notebook backend

set -e

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

exec uvicorn backend.views:app --reload --port 8001
