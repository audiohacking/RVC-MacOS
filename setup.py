"""
Setup script for building RVC-MacOS as a standalone macOS application.
Uses py2app to create a native .app bundle.

RVC-MacOS requires several model files to function:
- assets/hubert/hubert_base.pt
- assets/rmvpe/rmvpe.pt and rmvpe.onnx
- assets/pretrained/*.pth (12 files: D32k, D40k, D48k, G32k, G40k, G48k and f0 variants)
- assets/pretrained_v2/*.pth (12 files: same as above for v2)
- assets/uvr5_weights/*.pth (optional, for vocal separation)

These models must be downloaded before building or will be downloaded on first run.
"""

from setuptools import setup
import sys
import os

APP = ['launcher.py']  # Use launcher instead of web.py directly
DATA_FILES = [
    ('', ['.env', 'sha256.env']),  # Environment files needed for model verification
    ('assets', ['assets']),
    ('configs', ['configs']),
    ('i18n', ['i18n']),
    ('infer', ['infer']),
    ('rvc', ['rvc']),
    ('tools', ['tools']),
    ('docs', ['docs']),
]

# Note: Models are NOT pre-bundled - they will be downloaded on first run
print("\n" + "="*60)
print("RVC-MacOS Build Configuration")
print("="*60)
print("Models: NOT pre-bundled (downloaded on first run)")
print("This keeps the app bundle size smaller (~500MB vs ~2-3GB)")
print("\nOn first launch, the app will:")
print("  1. Check for required models")
print("  2. Download ~1.5GB of AI models (takes 5-10 minutes)")
print("  3. Start the web interface")
print("\nUsers will be informed of the download progress.")
print("="*60 + "\n")

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'gradio',
        'torch',
        'torchaudio',
        'torchvision',
        'numpy',
        'scipy',
        'librosa',
        'soundfile',
        'faiss',
        'sklearn',
        'flask',
        'fastapi',
        'uvicorn',
        'fairseq',
        'praat-parselmouth',
        'pyworld',
        'httpx',
        'pydantic',
        'starlette',
    ],
    'includes': [
        'web',
        'gui',
        'convert_audio',
        'download_models',
    ],
    'iconfile': 'assets/icon.icns',  # Icon file (will need to be created)
    'plist': {
        'CFBundleName': 'RVC-MacOS',
        'CFBundleDisplayName': 'RVC Voice Conversion',
        'CFBundleGetInfoString': 'Retrieval-based Voice Conversion for macOS',
        'CFBundleIdentifier': 'com.audiohacking.rvc-macos',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 AudioHacking. MIT License.',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '12.0',
        'NSRequiresAquaSystemAppearance': False,
    },
    'semi_standalone': False,
    'site_packages': True,
    'strip': False,
    'optimize': 0,
}

setup(
    name='RVC-MacOS',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version='1.0.0',
    description='Retrieval-based Voice Conversion for macOS',
    author='AudioHacking',
    license='MIT',
)
