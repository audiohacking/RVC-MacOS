# Packaging macOS Python Applications - RVC-MacOS Guide

This guide explains how to package the RVC-MacOS Python application as a native macOS application bundle (.app) and create distributable installers.

## Overview

RVC-MacOS uses `py2app` to create standalone macOS application bundles. This approach bundles Python, all dependencies, and application code into a single `.app` package that can be distributed to end users.

### RVC-Specific Requirements

RVC (Retrieval-based Voice Conversion) requires several large model files to function:

1. **HuBERT Model** (~189MB)
   - `assets/hubert/hubert_base.pt`
   - Used for feature extraction

2. **RMVPE Pitch Extraction Models** (~110MB total)
   - `assets/rmvpe/rmvpe.pt`
   - `assets/rmvpe/rmvpe.onnx`
   - Used for pitch detection

3. **Pretrained RVC Models v1** (~600MB total)
   - 12 files in `assets/pretrained/`:
   - D32k.pth, D40k.pth, D48k.pth (discriminators)
   - G32k.pth, G40k.pth, G48k.pth (generators)
   - f0D32k.pth, f0D40k.pth, f0D48k.pth (f0 discriminators)
   - f0G32k.pth, f0G40k.pth, f0G48k.pth (f0 generators)

4. **Pretrained RVC Models v2** (~600MB total)
   - Same 12 files in `assets/pretrained_v2/`

5. **UVR5 Weights** (optional, ~300MB)
   - Various files in `assets/uvr5_weights/`
   - Used for vocal/instrumental separation

**Total model size: ~1.5-2GB**

### Model Download Strategy

**Models are NOT pre-bundled in the app** - they are downloaded on first launch.

This approach:
- ✅ Keeps app bundle small (~500MB instead of ~3GB)
- ✅ Reduces GitHub bandwidth and storage costs
- ✅ Allows users to get updates to models independently
- ✅ Easier to maintain and distribute

**First Launch Process:**
1. User opens RVC-MacOS.app
2. `launcher.py` checks for models (finds none)
3. Displays clear message about download requirements
4. Downloads models (~1.5GB, takes 5-10 minutes)
5. Verifies checksums to ensure integrity
6. Starts web server on `http://localhost:7860`
7. Opens browser automatically
8. **Ready to use after ~10 minutes total on first launch**

**Subsequent Launches:**
- Models already present
- Starts immediately in 10-15 seconds

## Prerequisites

### System Requirements
- macOS 12.0 or later
- Apple Silicon (M1/M2/M3) or Intel Mac
- Python 3.8 to 3.10 (due to fairseq compatibility)
- Xcode Command Line Tools: `xcode-select --install`
- Homebrew (recommended): https://brew.sh

### Python Environment
```bash
# Check Python version
python3 --version  # Should be 3.8.x to 3.10.x

# Install system dependencies
brew install portaudio
```

## Building the Application

### Method 1: Automated Build Script (Recommended)

The easiest way to build the application:

```bash
# Make scripts executable (first time only)
chmod +x build_app.sh create_dmg.sh

# Build the application (~500MB without models)
./build_app.sh

# Create DMG installer
./create_dmg.sh
```

The build script will:
1. Check Python version (must be 3.8-3.10 due to fairseq dependency)
2. Create a virtual environment
3. Install all dependencies
4. Build the .app bundle
5. Place the result in `dist/RVC-MacOS.app`

**Note**: Models are NOT included in the build. They will be downloaded automatically when users first launch the app.

### Method 2: Manual Build

For more control over the build process:

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements/gui.txt
pip install py2app

# 3. Download models (if not already present)
python download_models.py

# 4. Build the application
python setup.py py2app

# 5. The built app will be in dist/RVC-MacOS.app
```

## Creating a DMG Installer

After building the app, create a distributable DMG:

```bash
./create_dmg.sh
```

This creates `dist/RVC-MacOS-Installer.dmg` which users can:
1. Download and open
2. Drag RVC-MacOS.app to Applications folder
3. Launch from Applications or Spotlight

## Application Structure

```
RVC-MacOS.app/
├── Contents/
│   ├── Info.plist              # App metadata
│   ├── MacOS/
│   │   └── launcher            # Main executable (from launcher.py)
│   ├── Resources/
│   │   ├── lib/                # Python runtime and packages
│   │   │   └── python3.x/
│   │   ├── .env                # Environment configuration
│   │   ├── sha256.env          # Model checksums for verification
│   │   ├── assets/             # Model files (if pre-bundled)
│   │   │   ├── hubert/
│   │   │   │   └── hubert_base.pt (~189MB)
│   │   │   ├── rmvpe/
│   │   │   │   ├── rmvpe.pt (~55MB)
│   │   │   │   └── rmvpe.onnx (~55MB)
│   │   │   ├── pretrained/     # 12 .pth files (~600MB)
│   │   │   ├── pretrained_v2/  # 12 .pth files (~600MB)
│   │   │   └── uvr5_weights/   # Optional vocal separation models
│   │   ├── configs/            # Configuration files
│   │   ├── infer/              # Inference modules
│   │   ├── rvc/                # RVC core modules
│   │   └── ...                 # Other app resources
│   └── Frameworks/             # Bundled frameworks
```

## First Launch Experience

### User's First-Time Experience

1. User downloads `RVC-MacOS-Installer.dmg` (~500MB)
2. Installs RVC-MacOS.app to Applications
3. Opens RVC-MacOS.app
4. Sees console window with clear messages:

```
============================================================
RVC-MacOS - Voice Conversion for Apple Silicon
============================================================

============================================================
FIRST-TIME SETUP: Downloading Required AI Models
============================================================

RVC requires AI model files to function.
These files will now be downloaded (~1.5GB).

What will be downloaded:
  • HuBERT base model (~189MB)
  • RMVPE pitch detection models (~110MB)
  • Pretrained RVC models v1 (~600MB)
  • Pretrained RVC models v2 (~600MB)

Estimated time: 5-10 minutes
This only happens once - models are saved for future use.

Please keep this window open and be patient...
============================================================

Starting download process...
[Download progress messages...]

============================================================
✓ SUCCESS! All models downloaded and verified!
============================================================

============================================================
Starting RVC Web Interface...
============================================================

The application will open in your default browser.
URL: http://localhost:7860

IMPORTANT: Keep this window open while using the app!
To stop the application, close this window or press Ctrl+C
============================================================
```

5. Browser opens automatically to `http://localhost:7860`
6. **Ready to use!**

### Subsequent Launches

1. User opens RVC-MacOS.app
2. Models already present (fast check)
3. Web server starts immediately
4. Browser opens to `http://localhost:7860`
5. **Ready in 10-15 seconds**

The launcher script (`launcher.py`) handles all of this automatically by:
- Calling `check_all_assets()` to verify models exist and are valid
- Calling `download_all_assets()` if any models are missing
- Providing clear, informative progress messages
- Waiting for download completion before starting web interface
- Handling errors gracefully with helpful messages

## Configuration Files

### setup.py

The `setup.py` file configures py2app with:
- **APP**: Main entry point (`web.py`)
- **DATA_FILES**: Resources to include (assets, configs, etc.)
- **OPTIONS**: py2app build options
  - `packages`: Python packages to include
  - `includes`: Python modules to include
  - `plist`: macOS app metadata (Info.plist)
  - `iconfile`: Application icon (`.icns` format)

Key settings:
```python
OPTIONS = {
    'packages': ['gradio', 'torch', ...],  # Dependencies
    'plist': {
        'CFBundleName': 'RVC-MacOS',
        'CFBundleIdentifier': 'com.audiohacking.rvc-macos',
        'LSMinimumSystemVersion': '12.0',
    },
    'iconfile': 'assets/icon.icns',
}
```

## Automated Builds with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/build-macos.yml`) that automatically builds and releases the app.

### Triggering Automated Builds

#### Option 1: Create a Git Tag
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will:
1. Build the app on GitHub's macOS runners
2. Create a DMG installer
3. Create a GitHub Release with the DMG attached

#### Option 2: Manual Workflow Dispatch
1. Go to the "Actions" tab in GitHub
2. Select "Build macOS App" workflow
3. Click "Run workflow"
4. Enter version number (optional)

### Workflow Steps
1. Checkout code
2. Set up Python 3.10
3. Install system dependencies
4. Install Python dependencies
5. Download models
6. Build application with py2app
7. Create DMG installer
8. Upload artifacts and create release

## Creating an Application Icon

macOS applications use `.icns` icon files. To create one:

### Using iconutil (Built-in macOS Tool)

1. Create PNG images at various sizes:
   - icon_16x16.png
   - icon_32x32.png
   - icon_64x64.png
   - icon_128x128.png
   - icon_256x256.png
   - icon_512x512.png
   - icon_1024x1024.png

2. Create iconset directory:
```bash
mkdir assets/icon.iconset
```

3. Copy images with proper naming:
```bash
cp icon_16x16.png assets/icon.iconset/icon_16x16.png
cp icon_32x32.png assets/icon.iconset/icon_16x16@2x.png
cp icon_32x32.png assets/icon.iconset/icon_32x32.png
cp icon_64x64.png assets/icon.iconset/icon_32x32@2x.png
# ... continue for all sizes
```

4. Convert to .icns:
```bash
iconutil -c icns assets/icon.iconset -o assets/icon.icns
```

### Using Online Tools
1. Create a 1024x1024 PNG icon
2. Use https://cloudconvert.com/png-to-icns
3. Save as `assets/icon.icns`

## Code Signing and Notarization (Optional)

For distribution outside the Mac App Store, apps should be signed and notarized.

### Requirements
- Apple Developer Account ($99/year)
- Developer ID Application certificate

### Signing
```bash
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  dist/RVC-MacOS.app
```

### Notarization
```bash
# Create app archive
ditto -c -k --keepParent dist/RVC-MacOS.app dist/RVC-MacOS.zip

# Submit for notarization
xcrun notarytool submit dist/RVC-MacOS.zip \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password"

# Staple notarization ticket
xcrun stapler staple dist/RVC-MacOS.app
```

## Distribution

### GitHub Releases
1. Build and create DMG
2. Create a git tag: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. GitHub Actions automatically creates release with DMG

### Manual Distribution
1. Build DMG with `./create_dmg.sh`
2. Share `dist/RVC-MacOS-Installer.dmg`
3. Users download, open DMG, drag app to Applications

## Troubleshooting

### Build Fails with Missing Dependencies
```bash
# Clean and rebuild
rm -rf build dist
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements/gui.txt
pip install py2app
python setup.py py2app
```

### App Won't Launch
1. Check Console.app for error messages
2. Test in Terminal:
```bash
./dist/RVC-MacOS.app/Contents/MacOS/RVC-MacOS
```

### "App is damaged and can't be opened"
This occurs when the app isn't signed. Users can bypass with:
```bash
xattr -cr /Applications/RVC-MacOS.app
```

Or developers should code sign the app.

### Missing Models
If models aren't included in the bundle:
```bash
python download_models.py
# Rebuild app
./build_app.sh
```

### Large App Size
The app bundle includes Python runtime and all dependencies. To reduce size:
- Remove unused packages from `setup.py` OPTIONS
- Use `strip: True` in py2app options (may break some packages)
- Compress DMG with higher compression

## Advanced Configuration

### Customizing py2app Options

Edit `setup.py` to modify build behavior:

```python
OPTIONS = {
    'argv_emulation': False,      # Don't emulate argv
    'semi_standalone': False,     # Include everything
    'site_packages': True,        # Include site-packages
    'strip': False,               # Don't strip symbols
    'optimize': 0,                # No optimization
    'iconfile': 'assets/icon.icns',
    'plist': {
        # Custom Info.plist entries
    },
}
```

### Including Additional Files

Add to `DATA_FILES` in `setup.py`:
```python
DATA_FILES = [
    ('assets', ['assets']),
    ('custom_folder', ['custom_folder']),
]
```

### Excluding Packages

Add to OPTIONS in `setup.py`:
```python
OPTIONS = {
    'excludes': ['package_to_exclude'],
    ...
}
```

## Performance Considerations

- **First Launch**: May be slow as the app unpacks resources
- **Startup Time**: Typically 5-10 seconds on Apple Silicon
- **Memory Usage**: ~2-4GB depending on models loaded
- **Disk Space**: App bundle ~1-2GB, additional space for models

## Best Practices

1. **Version Control**: Tag releases consistently (v1.0.0, v1.0.1, etc.)
2. **Testing**: Test built app on clean macOS installations
3. **Documentation**: Update README with download and installation instructions
4. **Changelog**: Maintain CHANGELOG.md for release notes
5. **Security**: Code sign and notarize for better user experience
6. **Updates**: Consider implementing auto-update mechanism

## Resources

- [py2app Documentation](https://py2app.readthedocs.io/)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [macOS Code Signing](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Homebrew](https://brew.sh)

## Support

For issues or questions:
- GitHub Issues: https://github.com/audiohacking/RVC-MacOS/issues
- Original RVC Project: https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI
