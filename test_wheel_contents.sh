#!/bin/bash
# Test script to verify wheel contents include reports module

echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info src/*.egg-info

echo "Building wheel..."
python -m pip install build 2>/dev/null || pip install build
python -m build --wheel

echo "Checking wheel contents..."
if [ -f dist/*.whl ]; then
    echo "Wheel built successfully!"
    echo ""
    echo "Checking for reports module in wheel:"
    unzip -l dist/*.whl | grep -E "flakestorm/reports" | head -10

    echo ""
    echo "All flakestorm packages in wheel:"
    unzip -l dist/*.whl | grep -E "flakestorm/.*__init__\.py" | sed 's/.*flakestorm\//  - flakestorm./' | sed 's/\/__init__\.py//'
else
    echo "ERROR: No wheel file found in dist/"
    exit 1
fi
