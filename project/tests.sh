#!/bin/bash

# Check if python3 is available
if command -v python3 &>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

# Run data pipeline
$PYTHON test_pipeline.py