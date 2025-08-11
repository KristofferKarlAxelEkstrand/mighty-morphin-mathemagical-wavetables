#!/bin/bash
# Auto-activate virtual environment for wavetable-generator project
# Source this file or add to your .bashrc

# Function to activate venv when in project directory
activate_wavetable_venv() {
    if [[ "$PWD" == *"/toffhub/wavetable-generator"* ]] && [ -d ".venv" ]; then
        if [[ "$VIRTUAL_ENV" != *"/toffhub/wavetable-generator/.venv"* ]]; then
            source .venv/Scripts/activate
            echo "Activated wavetable-generator virtual environment"
        fi
    fi
}

# Set PROMPT_COMMAND to check directory on each command
PROMPT_COMMAND="activate_wavetable_venv; $PROMPT_COMMAND"