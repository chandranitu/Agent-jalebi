#!/bin/bash

# Navigate to the project directory
cd /home/hadoop/Agent-jalebi

# Path to the virtual environment
VENV_PATH="/home/hadoop/venv-llm"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH"
    echo "Please create it using: python3.11 -m venv $VENV_PATH"
    exit 1
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Check if Ollama is running (optional but helpful)
if ! pgrep -x "ollama" > /dev/null; then
    echo "Warning: Ollama doesn't seem to be running. Make sure it's started."
fi

# Start the FastAPI application using uvicorn
echo "Starting Agent Jalebi on http://0.0.0.0:8081"
python3 main.py
