# Quick Start Guide - RVC-MacOS

This guide will help you get started with RVC-MacOS (Retrieval-based Voice Conversion) quickly.

## What is RVC-MacOS?

RVC-MacOS is a voice conversion application that allows you to:
- Convert voice recordings from one voice to another
- Train AI models on custom voices
- Process audio with high quality using Apple Silicon acceleration (MPS)
- Use a web-based interface for easy operation

**Important**: RVC requires ~1.5-2GB of AI model files to function. These will either be pre-bundled in the app or downloaded on first launch.

## For End Users (Download Pre-built App)

### Installation

1. **Download the App**
   - Go to [Releases](https://github.com/audiohacking/RVC-MacOS/releases)
   - Download `RVC-MacOS-Installer.dmg` (~500MB)

2. **Install the App**
   - Open the downloaded DMG file
   - Drag `RVC-MacOS.app` to your Applications folder
   - Close the DMG window

3. **First Launch** (Important!)
   - Open Applications folder
   - Double-click `RVC-MacOS.app`
   - If you see "cannot be opened because it is from an unidentified developer":
     - Right-click the app and select "Open"
     - Click "Open" in the dialog
     - Or go to System Preferences → Security & Privacy → General and click "Open Anyway"

4. **First-Time Model Download** ⚠️ IMPORTANT
   - A console/terminal window will appear with download progress
   - The app will download ~1.5GB of AI model files
   - **This takes 5-10 minutes** depending on your internet speed
   - **Keep the console window open!** Do not close it during download
   - You'll see clear progress messages:
     ```
     FIRST-TIME SETUP: Downloading Required AI Models
     • HuBERT base model (~189MB)
     • RMVPE pitch detection models (~110MB)
     • Pretrained RVC models v1 (~600MB)
     • Pretrained RVC models v2 (~600MB)
     Estimated time: 5-10 minutes
     ```
   - **Internet connection required** for first launch
   - This only happens once - models are saved for future use
   
5. **App Starts Automatically**
   - After models download, the web interface starts
   - A browser window opens at `http://localhost:7860`
   - If it doesn't open, manually visit `http://localhost:7860`
   - **Keep the console window open** while using the app
   - To stop the app, close the console window or press Ctrl+C

### Subsequent Launches
- Open RVC-MacOS.app (models already present)
- App starts in 10-15 seconds
- Browser opens automatically
- Ready to use immediately!

### Using the App

1. **Initial Setup (First Time)**
   - Wait for all models to download (if not pre-bundled)
   - The web interface will open at `http://localhost:7860`
   - You should see the RVC web interface with tabs for Model, Inference, Train, etc.

2. **Voice Conversion Workflow**
   - **Step 1**: Upload an audio file (WAV, MP3, etc.)
   - **Step 2**: Select a voice model (use pretrained or train your own)
   - **Step 3**: Adjust pitch (f0) and other parameters
   - **Step 4**: Click "Convert" to process
   - **Step 5**: Download the converted audio

3. **Training Your Own Voice Model**
   - Prepare audio files:
     - 10+ minutes of clean audio (WAV format recommended)
     - Single speaker, clear voice
     - Minimal background noise
     - 16kHz or higher sample rate
   - Use the "Train" tab in the web interface
   - Name your experiment (e.g., "my_voice")
   - Upload or select audio files
   - Start training (takes 30-60 minutes on Apple Silicon)
   - Use the trained model for conversion

4. **Understanding the Interface**
   - **Model Tab**: Manage and download voice models
   - **Inference Tab**: Convert voice in audio files
   - **Train Tab**: Train new voice models
   - **UVR5 Tab**: Separate vocals from instrumentals
   - **TTS Tab**: Text-to-speech features

## For Developers (Build from Source)

### Prerequisites

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.10
brew install python@3.10

# Install system dependencies
brew install portaudio
```

### Quick Build

```bash
# Clone the repository
git clone https://github.com/audiohacking/RVC-MacOS.git
cd RVC-MacOS

# Build the app (this creates .venv, installs deps, downloads models, and builds)
./build_app.sh

# Create DMG installer
./create_dmg.sh
```

The built app will be at `dist/RVC-MacOS.app` and the installer at `dist/RVC-MacOS-Installer.dmg`.

### Development Mode (Without Building)

If you want to run in development mode without building an app bundle:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements/gui.txt

# Download models
python download_models.py

# Run the app
python web.py

# Open browser to http://localhost:7860
```

## Troubleshooting

### App Won't Open
- **"App is damaged"**: Run `xattr -cr /Applications/RVC-MacOS.app` in Terminal
- **Permission denied**: Check System Preferences → Security & Privacy
- **"Python not found"**: This shouldn't happen with bundled app; rebuild if it does

### Models Not Downloading
- **Check internet connection**: Models are downloaded from Hugging Face
- **Firewall blocking**: Check if firewall is blocking the app
- **Disk space**: Ensure you have at least 3GB free space
- **Manual download**: See README.md for manual model download instructions
- **Retry**: Close app, delete `assets/` folders with incomplete models, restart

### Models Not Loading After Download
- **Verify checksums**: The app checks SHA256 hashes of model files
- **Corrupt downloads**: Delete the `assets` folder and restart to re-download
- **Check logs**: Look at the terminal/console window for error messages
- **File permissions**: Ensure the app has read/write access to its directories

### "No module named 'gradio'" or Similar Errors
- This means the app bundle is incomplete
- Rebuild the app: `rm -rf build dist && ./build_app.sh`
- Ensure all dependencies are installed before building

### Port Already in Use
- Another instance is running or another app is using port 7860
- Kill the process: `lsof -ti:7860 | xargs kill -9`
- Or specify a different port by editing `web.py` before building

### Performance Issues
- **RAM**: Ensure you're on a Mac with at least 8GB RAM (16GB recommended)
- **CPU**: Apple Silicon Macs (M1/M2/M3) perform significantly better than Intel
- **Background apps**: Close other resource-intensive applications
- **Training**: Voice model training can take 30-60 minutes on Apple Silicon
- **First conversion**: First conversion may be slower as models load into memory

### Audio Quality Issues
- **Use high-quality source**: 16kHz or higher sample rate
- **Clean audio**: Remove background noise before conversion
- **Adjust f0**: Pitch (f0) parameter needs tuning per voice
- **Try different models**: Experiment with v1 vs v2 pretrained models
- **Check RMVPE**: Use RMVPE pitch extraction for best results

### Build Fails
- **Python version**: Must be Python 3.8-3.10: `python3 --version`
  - RVC requires this due to fairseq dependency
  - Install correct version: `brew install python@3.10`
- **Missing dependencies**: `pip install -r requirements/gui.txt`
- **Clean build**: `rm -rf build dist .venv`
- **System dependencies**: `brew install portaudio`
- **Try again**: `./build_app.sh`

### App Crashes on Launch
- **Check Console.app**: Look for crash logs and error messages
- **Test in Terminal**: Run `./dist/RVC-MacOS.app/Contents/MacOS/launcher`
- **Missing models**: Ensure models downloaded correctly
- **Memory**: Close other apps if you have low RAM
- **Rebuild**: Try `rm -rf build dist && ./build_app.sh`

## Getting Help

- **Issues**: https://github.com/audiohacking/RVC-MacOS/issues
- **Documentation**: See [PACKAGING_MACOS_PYTHON_APPS.md](./PACKAGING_MACOS_PYTHON_APPS.md)
- **Original Project**: https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI

## Tips

1. **Better Results**: Use high-quality, clean audio recordings for training
2. **Training Time**: Expect 30-60 minutes for training on Apple Silicon
3. **Disk Space**: Keep at least 10GB free for models and training data
4. **Updates**: Check the Releases page regularly for new versions
5. **Backups**: Save your trained models regularly (found in `logs/` folder)

## Next Steps

- Read the full [README.md](./README.md) for more features
- Check out the [PACKAGING_MACOS_PYTHON_APPS.md](./PACKAGING_MACOS_PYTHON_APPS.md) for build details
- Explore training options in the web interface
- Try different pitch extraction algorithms for best results
