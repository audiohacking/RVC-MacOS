#!/bin/bash

# Build script for RVC-MacOS application
# This script creates a standalone macOS .app bundle

set -e

echo "Building RVC-MacOS application..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo "Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.8" ]] || [[ "$PYTHON_VERSION" > "3.10" ]]; then
    echo "Error: Python version must be between 3.8 and 3.10"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements/gui.txt

# Install py2app
echo "Installing py2app..."
pip install py2app

# Clean previous build
echo "Cleaning previous build..."
rm -rf build dist

# Download models if not present
if [ ! -f "assets/hubert/hubert_base.pt" ]; then
    echo "Downloading models..."
    python download_models.py
fi

# Build the app
echo "Building application bundle..."
python setup.py py2app

echo ""
echo "Build complete!"
echo "Application bundle created at: dist/RVC-MacOS.app"
echo ""
echo "To create a DMG installer, run: ./create_dmg.sh"
