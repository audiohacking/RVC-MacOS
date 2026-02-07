<div align="center">

# Retrieval-based-Voice-Conversion-WebUI
An easy-to-use voice conversion framework based on VITS - for MacOS



[![madewithlove](https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=orange
)](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI)

[![Licence](https://img.shields.io/github/license/fumiama/Retrieval-based-Voice-Conversion-WebUI?style=for-the-badge)](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)
[![Huggingface](https://img.shields.io/badge/🤗%20-Spaces-yellow.svg?style=for-the-badge)](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

[![Discord](https://img.shields.io/badge/RVC%20Developers-Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/HcsmBBGyVk)

[**FAQ (Frequently Asked Questions)**](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI/wiki/FAQ-(Frequently-Asked-Questions)) 

[**English**](./README.md) | [**中文简体**](./docs/cn/README.cn.md) | [**日本語**](./docs/jp/README.ja.md) | [**한국어**](./docs/kr/README.ko.md) ([**韓國語**](./docs/kr/README.ko.han.md)) | [**Français**](./docs/fr/README.fr.md) | [**Türkçe**](./docs/tr/README.tr.md) | [**Português**](./docs/pt/README.pt.md)

</div>

> The base model is trained using nearly 50 hours of high-quality open-source VCTK training set. Therefore, there are no copyright concerns, please feel free to use.

> Please look forward to the base model of RVCv3 with larger parameters, larger dataset, better effects, basically flat inference speed, and less training data required.

> There's a [one-click downloader](https://github.com/fumiama/RVC-Models-Downloader) for models/integration packages/tools. Welcome to try.

| Training and inference Webui |
| :--------: |
| ![web](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI/assets/41315874/17e48404-2627-4fad-a0ec-65f9065aeade) |

| Real-time voice changing GUI |
| :---------: |
| ![realtime-gui](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI/assets/41315874/95b36866-b92d-40c7-b5db-6a35ca5caeac) |

## Features:
+ Reduce tone leakage by replacing the source feature to training-set feature using top1 retrieval;
+ Easy + fast training, even on Apple Silicon;
+ Training with a small amounts of data (>=10min low noise speech recommended);
+ Model fusion to change timbres (using ckpt processing tab->ckpt merge);
+ Easy-to-use WebUI;
+ UVR5 model to quickly separate vocals and instruments;
+ High-pitch Voice Extraction Algorithm [InterSpeech2023-RMVPE](#Credits) to prevent a muted sound problem. Provides the best results (significantly) and is faster with lower resource consumption than Crepe_full;
+ Apple Silicon acceleration with MPS (Metal Performance Shaders) supported.

Check out our [Demo Video](https://www.bilibili.com/video/BV1pm4y1z7Gm/) here!

## 📦 Standalone macOS Application

**New!** RVC-MacOS is now available as a standalone macOS application bundle (.app) that can be distributed without requiring users to install Python or dependencies.

### Download Pre-built App
Download the latest release from [GitHub Releases](https://github.com/audiohacking/RVC-MacOS/releases):
1. Download `RVC-MacOS-Installer.dmg` (~500MB)
2. Open the DMG file
3. Drag `RVC-MacOS.app` to your Applications folder
4. Launch from Applications or Spotlight

**Important - First Launch**:
- **First-time setup takes 5-10 minutes** to download AI models
- The app will download ~1.5GB of required model files automatically
- You'll see clear progress messages during the download
- **Internet connection required** for first launch
- Subsequent launches are instant (models are saved)

### What Gets Downloaded on First Launch

RVC requires AI model files to function. On first launch, the app automatically downloads:
- **HuBERT base model** (~189MB): Voice feature extraction
- **RMVPE pitch models** (~110MB): Pitch detection
- **Pretrained RVC models v1** (~600MB): Voice conversion
- **Pretrained RVC models v2** (~600MB): Enhanced voice conversion

**Total**: ~1.5GB downloaded once, used forever

**Disk space needed**: At least 3GB free (for models + temporary files)

### Build from Source
To build the standalone application yourself:

```bash
# Quick build - creates ~500MB app bundle
./build_app.sh

# Create DMG installer
./create_dmg.sh
```

The build script will:
1. Check for Python 3.8-3.10 (required by fairseq)
2. Install dependencies
3. Build the .app bundle (~500MB without models)
4. Models will be downloaded by end users on first launch

The built application will be in `dist/RVC-MacOS.app` and the DMG installer in `dist/RVC-MacOS-Installer.dmg`.

For detailed build instructions, see [PACKAGING_MACOS_PYTHON_APPS.md](./PACKAGING_MACOS_PYTHON_APPS.md).

---

## Environment Configuration
### Python Version Limitation
> It is recommended to use venv to manage the Python environment.

> For the reason of the version limitation, please refer to this [bug](https://github.com/facebookresearch/fairseq/issues/5012).

```bash
python --version # 3.8 <= Python < 3.11
```

### MacOS One-click Dependency Installation & Startup Script
By executing `run.sh` in the project root directory, you can configure the `venv` virtual environment, automatically install the required dependencies, and start the main program with one click.

#### Quick Start (without models)
```bash
sh ./run.sh
```
This will start the application. If models are missing, you'll need to download them first - see "Automatic Download" under the Assets section below.

#### First-time Setup (with automatic model download)
```bash
sh ./run.sh --download-models
```
This will download all required models before starting the application. This is recommended for first-time setup and may take several minutes depending on your internet connection.

### Manual Installation of Dependencies
1. Install `pytorch` and its core dependencies, skip if already installed. Refer to: https://pytorch.org/get-started/locally/
	```bash
	pip install torch torchvision torchaudio
	```

2. Install the required dependencies:
	```bash
	pip install -r requirements/gui.txt
	```

## Preparation of Other Files
### 1. Assets
> RVC requires some models located in the `assets` folder for inference and training.

#### Automatic Download (Recommended)
The easiest way to download all required models is using the included download script:
```bash
python download_models.py
```

Or use the run.sh script with the --download-models flag:
```bash
sh ./run.sh --download-models
```

#### Check/Download via Web Interface
> By default, RVC can automatically check the integrity of the required resources when the main program starts.

> Even if the resources are not complete, the program will continue to start.

- If you want to download all resources when starting the web interface, please add the `--update` parameter:
  ```bash
  python web.py --update
  ```
- If you want to skip the resource integrity check at startup, please add the `--nocheck` parameter.

#### Download Manually
> All resource files are located in [Hugging Face space](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

> You can find some scripts to download them in the `tools` folder

> You can also use the [one-click downloader](https://github.com/fumiama/RVC-Models-Downloader) for models/integration packages/tools

Below is a list that includes the names of all pre-models and other files required by RVC.

- ./assets/hubert/hubert_base.pt
	```bash
	rvcmd assets/hubert # RVC-Models-Downloader command
	```
- ./assets/pretrained
	```bash
	rvcmd assets/v1 # RVC-Models-Downloader command
	```
- ./assets/uvr5_weights
	```bash
	rvcmd assets/uvr5 # RVC-Models-Downloader command
	```
If you want to use the v2 version of the model, you need to download additional resources in

- ./assets/pretrained_v2
	```bash
	rvcmd assets/v2 # RVC-Models-Downloader command
	```

### 2. Download the required files for the rmvpe vocal pitch extraction algorithm

If you want to use the latest RMVPE vocal pitch extraction algorithm, you need to download the pitch extraction model parameters and place them in `assets/rmvpe`.

- [rmvpe.pt](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/rmvpe.pt)
	```bash
	rvcmd assets/rmvpe # RVC-Models-Downloader command
	```

## Getting Started
### MacOS (Recommended)
For first-time setup with automatic model download:
```bash
./run.sh --download-models
```

For subsequent runs:
```bash
./run.sh
```

### Direct Launch
Use the following command to start the WebUI.
```bash
python web.py
```

To download all required models before starting:
```bash
python web.py --update
```

## Credits
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [Vocal pitch extraction:RMVPE](https://github.com/Dream-High/RMVPE)
  + The pretrained model is trained and tested by [yxlllc](https://github.com/yxlllc/RMVPE) and [RVC-Boss](https://github.com/RVC-Boss).

## Thanks to all contributors for their efforts
[![contributors](https://contrib.rocks/image?repo=fumiama/Retrieval-based-Voice-Conversion-WebUI)](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors)

# RVC-WebUI-MacOS

A macOS-optimized version of the Retrieval-based Voice Conversion WebUI, specifically designed for Apple Silicon (M1/M2/M3) Macs.

## Features

- Voice conversion with high-quality results
- Easy automated setup with automatic model download
- Optimized for Apple Silicon (M1/M2/M3) Macs
- User-friendly web interface
- Support for various audio formats
- Real-time voice conversion
- Training capabilities for custom voice models

## Requirements

- macOS 12.0 or later
- Apple Silicon Mac (M1/M2/M3)
- Python 3.8 to 3.10 (due to fairseq compatibility, see [bug](https://github.com/facebookresearch/fairseq/issues/5012))
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

## Installation

### Option 1: Quick Setup with run.sh (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/audiohacking/RVC-WebUI-MacOS.git
cd RVC-WebUI-MacOS
```

2. Run the setup script with automatic model download:
```bash
sh ./run.sh --download-models
```

This will automatically:
- Create a virtual environment
- Install all dependencies
- Download all required models
- Start the web interface

### Option 2: Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/audiohacking/RVC-WebUI-MacOS.git
cd RVC-WebUI-MacOS
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements/gui.txt
```

4. Download models:
```bash
python web.py --update
```

## Usage

### Using run.sh (Recommended)
```bash
./run.sh
```

### Manual Launch
1. Activate the virtual environment:
```bash
source .venv/bin/activate
```

2. Start the web interface:
```bash
python web.py --port 7860
```

3. Open your web browser and navigate to:
```
http://localhost:7860
```

## Training Your Own Model

1. Prepare your training data:
   - Place your audio files in WAV format
   - Recommended duration: 10-50 minutes of clean audio
   - Sample rate: 16kHz or higher
   - Place files in `logs/your_experiment_name/0_gt_wavs/`

2. Start training:
   - Use the web interface to start training
   - Select your experiment name
   - Choose training parameters
   - Click "Start Training"

## Directory Structure

```
RVC-WebUI-MacOS/
├── assets/
│   ├── pretrained/    # Pretrained models (included)
│   └── rmvpe/         # RMVPE model files (included)
├── logs/
│   └── your_experiment_name/
│       ├── 0_gt_wavs/     # Original audio files
│       ├── 1_16k_wavs/    # 16kHz converted files
│       ├── 2a_f0/         # Pitch information
│       └── 2b-f0nsf/      # Processed pitch information
├── requirements/
│   └── gui.txt        # GUI dependencies
└── web.py             # Main application file
```

## Troubleshooting

1. If you encounter "No supported Nvidia GPU found" message:
   - This is normal for M-series Macs
   - The application will automatically use MPS (Metal Performance Shaders)

2. If you get "address already in use" error:
   - Try using a different port: `python web.py --port 7861`

3. If model loading fails:
   - Verify file permissions
   - Check if the model files are present in the assets directory
   - Try reinstalling the dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original project: [fumiama-Retrieval-based-Voice-Conversion-WebUI](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI)
- Modified and optimized for macOS by Nevil Patel
