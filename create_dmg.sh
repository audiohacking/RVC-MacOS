#!/bin/bash

# Script to create a DMG installer for RVC-MacOS
# This creates a distributable disk image for easy installation

set -e

APP_NAME="RVC-MacOS"
DMG_NAME="${APP_NAME}-Installer"
VERSION="1.0.0"
APP_PATH="dist/${APP_NAME}.app"
DMG_PATH="dist/${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME} ${VERSION}"

echo "Creating DMG installer for ${APP_NAME}..."

# Check if app bundle exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: Application bundle not found at $APP_PATH"
    echo "Please run ./build_app.sh first"
    exit 1
fi

# Remove old DMG if it exists
if [ -f "$DMG_PATH" ]; then
    echo "Removing old DMG..."
    rm "$DMG_PATH"
fi

# Create temporary directory for DMG contents
DMG_TEMP="dist/dmg_temp"
rm -rf "$DMG_TEMP"
mkdir -p "$DMG_TEMP"

# Copy app to temp directory
echo "Copying application bundle..."
cp -R "$APP_PATH" "$DMG_TEMP/"

# Create symbolic link to Applications folder
echo "Creating Applications symlink..."
ln -s /Applications "$DMG_TEMP/Applications"

# Create DMG
echo "Creating disk image..."
hdiutil create -volname "$VOLUME_NAME" \
    -srcfolder "$DMG_TEMP" \
    -ov -format UDZO \
    "$DMG_PATH"

# Clean up temp directory
rm -rf "$DMG_TEMP"

echo ""
echo "DMG created successfully!"
echo "Location: $DMG_PATH"
echo ""
echo "To install, open the DMG and drag ${APP_NAME}.app to Applications"
