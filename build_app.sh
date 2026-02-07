#!/bin/bash

# Build script for RVC-MacOS application
# This script creates a standalone macOS .app bundle
#
# RVC-MacOS requires several large model files:
# - assets/hubert/hubert_base.pt (~189MB)
# - assets/rmvpe/rmvpe.pt + rmvpe.onnx (~110MB total)
# - assets/pretrained/*.pth (12 files, ~600MB total)
# - assets/pretrained_v2/*.pth (12 files, ~600MB total)
# - assets/uvr5_weights/*.pth (optional, for vocal separation)
#
# Total size: ~1.5GB+ of model files
# Final .app bundle size: ~2-3GB (includes Python, dependencies, and models)

set -e

echo "Building RVC-MacOS application..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo "Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.8" ]] || [[ "$PYTHON_VERSION" > "3.10" ]]; then
    echo "Error: Python version must be between 3.8 and 3.10"
    echo "Current version: $PYTHON_VERSION"
    echo ""
    echo "RVC requires Python 3.8-3.10 due to fairseq compatibility."
    echo "See: https://github.com/facebookresearch/fairseq/issues/5012"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements/gui.txt

# Install py2app
echo ""
echo "Installing py2app..."
pip install py2app

# Clean previous build
echo ""
echo "Cleaning previous build..."
rm -rf build dist

# Note about models - they are NOT pre-bundled
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Build Strategy: Models NOT Pre-bundled"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Models will be downloaded on first app launch."
echo "This keeps the app bundle size smaller (~500MB vs ~2-3GB)."
echo ""
echo "On first launch, users will see:"
echo "  - Clear notification about model download"
echo "  - Download progress (~1.5GB of AI models)"
echo "  - Estimated time: 5-10 minutes depending on connection"
echo ""
echo "The app will automatically download these models:"
echo "  - HuBERT base model (~189MB)"
echo "  - RMVPE pitch models (~110MB)"
echo "  - Pretrained RVC models v1 (~600MB)"
echo "  - Pretrained RVC models v2 (~600MB)"
echo ""
echo "Total download: ~1.5GB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Build the app
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Building application bundle..."
echo "This will take several minutes..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python setup.py py2app

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Build complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Application bundle created at: dist/RVC-MacOS.app"
echo ""
echo "You can now:"
echo "  1. Run the app: open dist/RVC-MacOS.app"
echo "  2. Create DMG installer: ./create_dmg.sh"
echo ""
