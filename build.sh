#!/bin/bash
set -e

echo "=== Building tools.neurohackingly.com ==="

# Create dist directory
mkdir -p dist

# Install dependencies if needed
echo "Installing Python dependencies..."
pip install --quiet pyyaml jinja2 markdown beautifulsoup4 2>/dev/null || true

# Build the index
echo "Building index..."
python3 build_index.py

echo "=== Build complete! ==="
