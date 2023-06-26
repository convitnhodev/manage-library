#!/bin/bash

# Create a new virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate

# Install libraries from requirements.txt
pip install -r requirements.txt
