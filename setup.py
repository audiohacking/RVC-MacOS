"""
Setup script for building RVC-MacOS as a standalone macOS application.
Uses py2app to create a native .app bundle.

RVC-MacOS requires several model files to function:
- assets/hubert/hubert_base.pt
- assets/rmvpe/rmvpe.pt and rmvpe.onnx
- assets/pretrained/*.pth (12 files: D32k, D40k, D48k, G32k, G40k, G48k and f0 variants)
- assets/pretrained_v2/*.pth (12 files: same as above for v2)
- assets/uvr5_weights/*.pth (optional, for vocal separation)

These models will be downloaded on first run.

IMPORTANT: This build includes ALL Python dependencies. Users don't need to install anything.
"""

from setuptools import setup
import sys
import os

APP = ["launcher.py"]  # Use launcher instead of web.py directly
DATA_FILES = [
    ("", [".env", "sha256.env"]),  # Environment files needed for model verification
    ("assets", ["assets"]),
    ("configs", ["configs"]),
    ("i18n", ["i18n"]),
    ("infer", ["infer"]),
    ("rvc", ["rvc"]),
    ("tools", ["tools"]),
    ("docs", ["docs"]),
]

# Note: Models are NOT pre-bundled - they will be downloaded on first run
print("\n" + "=" * 60)
print("RVC-MacOS Build Configuration")
print("=" * 60)
print("Python Dependencies: ALL INCLUDED (fully standalone)")
print("Models: NOT pre-bundled (downloaded on first run)")
print("\nThis keeps the app bundle size at ~500MB")
print("Models (~1.5GB) are downloaded on first launch")
print("\nOn first launch, the app will:")
print("  1. Check for required models")
print("  2. Download ~1.5GB of AI models (takes 5-10 minutes)")
print("  3. Start the web interface")
print("\nUsers will NOT need to install Python or any dependencies!")
print("=" * 60 + "\n")

# Comprehensive package list - EVERYTHING must be included in the frozen app
# Users should NOT need to install anything manually
OPTIONS = {
    "argv_emulation": False,
    "packages": [
        # Core PyTorch and related (SECURITY: >= 2.6.0 for vulnerability fixes)
        "torch",
        "torchvision",
        "torchaudio",
        "torchcrepe",
        "torchfcpe",
        # Web frameworks
        "gradio",
        "flask",
        "flask_cors",
        "fastapi",
        "uvicorn",
        "starlette",
        "httpx",
        # Scientific computing
        "numpy",
        "scipy",
        "scikit_learn",
        "sklearn",
        # Audio processing
        "librosa",
        "soundfile",
        "resampy",
        "audioread",
        "pydub",
        "pyworld",
        "praat-parselmouth",
        "sounddevice",
        "noisereduce",
        "av",
        # ML/AI frameworks
        "fairseq",
        "faiss",
        "onnxruntime",
        # Utilities
        "einops",
        "numba",
        "llvmlite",
        "Cython",
        "gin",
        "gin_config",
        "local_attention",
        "tqdm",
        "joblib",
        "tensorboard",
        "tensorboardX",
        # Web and data
        "pydantic",
        "PyYAML",
        "json5",
        "Markdown",
        "Jinja2",
        "Pillow",
        "matplotlib",
        "matplotlib-inline",
        # System
        "wave",
        "dotenv",
        "pybase16384",
        "colorama",
        "tabulate",
        "fsspec",
        "sympy",
        "tornado",
        "Werkzeug",
        "absl-py",
        "pyasn1",
        "pyasn1-modules",
        "uc-micro-py",
        # GUI (if needed)
        "FreeSimpleGUI",
    ],
    "includes": [
        # Explicitly include main modules
        "web",
        "gui",
        "convert_audio",
        "download_models",
        # Include all submodules
        "infer.lib.rvcmd",
        "infer.lib.audio",
        "infer.lib.rtrvc",
        "infer.lib.train.data_utils",
        "infer.modules.vc.pipeline",
        "rvc.synthesizer",
        "rvc.f0",
        "rvc.hubert",
        "rvc.layers",
        # Ensure all imports are included
        "encodings.idna",
        "encodings.utf_8",
        "email.mime",
        "email.mime.text",
        "email.mime.multipart",
        "email.mime.base",
        "logging.handlers",
    ],
    "excludes": [
        # Exclude test and doc modules to reduce size
        "test",
        "tests",
        "testing",
        "unittest",
        "pydoc",
        "tkinter",
    ],
    "frameworks": [],
    "iconfile": "assets/icon.icns",  # Icon file (will create if needed)
    "plist": {
        "CFBundleName": "RVC-MacOS",
        "CFBundleDisplayName": "RVC Voice Conversion",
        "CFBundleGetInfoString": "Retrieval-based Voice Conversion for macOS",
        "CFBundleIdentifier": "com.audiohacking.rvc-macos",
        "CFBundleVersion": "0.0.1",
        "CFBundleShortVersionString": "0.0.1",
        "NSHumanReadableCopyright": "Copyright © 2024 AudioHacking. MIT License.",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "12.0",
        "NSRequiresAquaSystemAppearance": False,
        "NSAppTransportSecurity": {
            "NSAllowsArbitraryLoads": True  # Allow model downloads from internet
        },
    },
    "semi_standalone": False,  # Fully standalone - include everything
    "site_packages": True,  # Include site-packages
    "strip": False,  # Don't strip symbols (helps with debugging)
    "optimize": 0,  # No optimization for better compatibility
    "matplotlib_backends": ["macosx"],  # Include macOS matplotlib backend
    "resources": [],
    "emulate_shell_environment": False,
}

setup(
    name="RVC-MacOS",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    version="0.0.1",
    description="Retrieval-based Voice Conversion for macOS",
    author="AudioHacking",
    license="MIT",
)
