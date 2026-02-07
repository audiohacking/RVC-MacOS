#!/usr/bin/env python3
"""
Launcher script for RVC-MacOS standalone application.
This script serves as the main entry point for the .app bundle.
"""

import sys
import os

# Set up the environment for the bundled app
if getattr(sys, 'frozen', False):
    # Running in a bundle
    bundle_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    os.chdir(os.path.dirname(bundle_dir))

# Import and run the main web application
if __name__ == '__main__':
    # Add any app-specific initialization here
    import web
    # The web.py module will handle the rest
