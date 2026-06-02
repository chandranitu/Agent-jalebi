#!/bin/bash

# Navigate to the project directory
cd /home/hadoop/Agent-jalebi

# Path to the virtual environment
VENV_PATH="/home/hadoop/venv-llm"

echo "Setting up environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    python3.11 -m venv "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install openai-whisper python-multipart pydantic-settings uvicorn fastapi psycopg2-binary ollama

echo "Setup complete. You can now start the application using ./start.sh"
