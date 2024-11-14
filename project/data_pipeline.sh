#!/bin/bash

# Check if python3 is available
if command -v python3 &>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

# Install dependencies
$PYTHON -m pip install -r requirements.txt

# Set Kaggle config directory
export KAGGLE_CONFIG_DIR=~/.kaggle

# Check if Kaggle API key is available
if [ ! -f "$KAGGLE_CONFIG_DIR/kaggle.json" ]; then
  echo "Error: Kaggle API key file 'kaggle.json' not found in $KAGGLE_CONFIG_DIR."
  echo "Please ensure you have placed your 'kaggle.json' file in the '$KAGGLE_CONFIG_DIR' directory."
  echo "For more information visit 'https://github.com/Kaggle/kaggle-api'"
  exit 1
else
  echo "Kaggle API dependency available."
fi

# Run data pipeline
$PYTHON data_pipeline.py

