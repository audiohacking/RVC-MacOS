#!/usr/bin/env python3
"""
Launcher script for RVC-MacOS standalone application.
This script serves as the main entry point for the .app bundle.

RVC requires several model files to function. This launcher will:
1. Check if required models are present
2. Download models if missing (on first run)
3. Start the web interface

Required models:
- assets/hubert/hubert_base.pt (~189MB)
- assets/rmvpe/rmvpe.pt (~55MB) 
- assets/rmvpe/rmvpe.onnx (~55MB)
- assets/pretrained/*.pth (12 files, ~50MB each)
- assets/pretrained_v2/*.pth (12 files, ~50MB each)
"""

import sys
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment for the bundled app."""
    if getattr(sys, 'frozen', False):
        # Running in a bundle - get the bundle directory
        if hasattr(sys, '_MEIPASS'):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(sys.executable)
        
        # Change to the Resources directory which contains our app files
        resources_dir = os.path.join(bundle_dir, '..', 'Resources')
        if os.path.exists(resources_dir):
            os.chdir(resources_dir)
            logger.info(f"Changed directory to: {os.getcwd()}")
        else:
            os.chdir(bundle_dir)
            logger.info(f"Changed directory to: {os.getcwd()}")
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())

def check_and_download_models():
    """Check if required models exist and download if missing."""
    from dotenv import load_dotenv
    import shutil
    
    # Load environment variables for model verification
    load_dotenv()
    load_dotenv("sha256.env")
    
    # Import model checking functions
    try:
        from infer.lib.rvcmd import check_all_assets, download_all_assets
    except ImportError as e:
        logger.error(f"Failed to import model management functions: {e}")
        logger.error("The application may not function correctly.")
        return False
    
    logger.info("Checking for required model files...")
    
    # Check if models are present
    if check_all_assets(update=False):
        logger.info("✓ All required models are present!")
        return True
    
    # Models are missing - inform user about download
    logger.info("")
    logger.info("="*60)
    logger.info("FIRST-TIME SETUP: Downloading Required AI Models")
    logger.info("="*60)
    logger.info("")
    logger.info("RVC requires AI model files to function.")
    logger.info("These files will now be downloaded (~1.5GB).")
    logger.info("")
    logger.info("What will be downloaded:")
    logger.info("  • HuBERT base model (~189MB)")
    logger.info("  • RMVPE pitch detection models (~110MB)")
    logger.info("  • Pretrained RVC models v1 (~600MB)")
    logger.info("  • Pretrained RVC models v2 (~600MB)")
    logger.info("")
    logger.info("Estimated time: 5-10 minutes")
    logger.info("This only happens once - models are saved for future use.")
    logger.info("")
    logger.info("Please keep this window open and be patient...")
    logger.info("="*60)
    logger.info("")
    
    # Create temp directory for downloads
    now_dir = os.getcwd()
    tmp = os.path.join(now_dir, "TEMP")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    
    try:
        # Download all required assets
        logger.info("Starting download process...")
        download_all_assets(tmpdir=tmp)
        
        # Verify download was successful
        logger.info("")
        logger.info("Verifying downloaded models...")
        if check_all_assets(update=True):
            logger.info("")
            logger.info("="*60)
            logger.info("✓ SUCCESS! All models downloaded and verified!")
            logger.info("="*60)
            logger.info("")
            return True
        else:
            logger.warning("")
            logger.warning("="*60)
            logger.warning("⚠ Some models may not have downloaded correctly.")
            logger.warning("The application will start but may have limited functionality.")
            logger.warning("You can try restarting the app to re-download missing models.")
            logger.warning("="*60)
            logger.warning("")
            return False
    except Exception as e:
        logger.error("")
        logger.error("="*60)
        logger.error(f"✗ Error downloading models: {e}")
        logger.error("="*60)
        logger.error("")
        logger.error("Possible causes:")
        logger.error("  • No internet connection")
        logger.error("  • Firewall blocking downloads")
        logger.error("  • Insufficient disk space (need ~3GB free)")
        logger.error("  • Network timeout")
        logger.error("")
        logger.error("You can:")
        logger.error("  1. Check your internet connection and try again")
        logger.error("  2. See documentation for manual model download")
        logger.error("")
        return False
    finally:
        # Cleanup temp directory
        shutil.rmtree(tmp, ignore_errors=True)

def main():
    """Main entry point for RVC-MacOS application."""
    logger.info("="*60)
    logger.info("RVC-MacOS - Voice Conversion for Apple Silicon")
    logger.info("="*60)
    
    # Set up environment
    setup_environment()
    
    # Check and download models if needed
    logger.info("")
    models_ready = check_and_download_models()
    
    if not models_ready:
        logger.warning("")
        logger.warning("WARNING: Not all models are available!")
        logger.warning("The application will start but may not function correctly.")
        logger.warning("Please restart the app to retry downloading models.")
        logger.warning("")
        input("Press Enter to continue anyway, or close this window to exit...")
    
    # Start the web interface
    logger.info("")
    logger.info("="*60)
    logger.info("Starting RVC Web Interface...")
    logger.info("="*60)
    logger.info("")
    logger.info("The application will open in your default browser.")
    logger.info("URL: http://localhost:7860")
    logger.info("")
    logger.info("IMPORTANT: Keep this window open while using the app!")
    logger.info("To stop the application, close this window or press Ctrl+C")
    logger.info("="*60)
    logger.info("")
    
    try:
        # Import and run the main web application
        import web
        # web.py will handle the rest and keep running
    except KeyboardInterrupt:
        logger.info("")
        logger.info("="*60)
        logger.info("Shutting down RVC-MacOS...")
        logger.info("="*60)
        sys.exit(0)
    except Exception as e:
        logger.error("")
        logger.error("="*60)
        logger.error(f"Error starting application: {e}")
        logger.error("="*60)
        logger.error("")
        logger.error("Please check the logs above for more information.")
        logger.error("If the problem persists, see:")
        logger.error("https://github.com/audiohacking/RVC-MacOS/issues")
        logger.error("")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
