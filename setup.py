"""
Setup script for building RVC-MacOS as a standalone macOS application.
Uses py2app to create a native .app bundle.
"""

from setuptools import setup
import sys

APP = ['web.py']
DATA_FILES = [
    ('assets', ['assets']),
    ('configs', ['configs']),
    ('i18n', ['i18n']),
    ('infer', ['infer']),
    ('rvc', ['rvc']),
    ('tools', ['tools']),
    ('docs', ['docs']),
]

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
