#!/usr/bin/env python3
"""
Script to download all required models for RVC-WebUI-MacOS.
This script downloads models without starting the web interface.
"""

import os
import sys
import shutil
from dotenv import load_dotenv

# Add current directory to path
now_dir = os.getcwd()
sys.path.append(now_dir)

# Load environment variables
load_dotenv()
load_dotenv("sha256.env")

# Create temp directory
tmp = os.path.join(now_dir, "TEMP")
shutil.rmtree(tmp, ignore_errors=True)
os.makedirs(tmp, exist_ok=True)

# Import model checking and downloading functions
from infer.lib.rvcmd import check_all_assets, download_all_assets

print("=" * 60)
print("RVC-WebUI-MacOS Model Downloader")
print("=" * 60)
print()

# Check if models are already present
print("Checking for existing models...")
if check_all_assets(update=False):
    print("✓ All required models are already present!")
    print("  No download needed.")
    sys.exit(0)

print()
print("Some models are missing or outdated.")
print("Starting download process...")
print("This may take several minutes depending on your connection.")
print()

try:
    # Download all assets
    download_all_assets(tmpdir=tmp)

    # Verify download was successful
    print()
    print("Verifying downloaded models...")
    if check_all_assets(update=True):
        print()
        print("=" * 60)
        print("✓ SUCCESS! All models downloaded successfully!")
        print("=" * 60)
        print()
        print("You can now run: ./run.sh")
        sys.exit(0)
    else:
        print()
        print("⚠ Warning: Some models may not have downloaded correctly.")
        print("  You may want to try running this script again.")
        print("  The application may have limited functionality without all models.")
        sys.exit(2)

except Exception as e:
    print()
    print(f"✗ Error during download: {e}")
    print("  You can try running this script again, or download models manually.")
    print("  See README.md for manual download instructions.")
    sys.exit(1)
finally:
    # Cleanup
    shutil.rmtree(tmp, ignore_errors=True)
