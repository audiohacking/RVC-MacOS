#!/bin/sh

set -fa

# Check if Python is installed
if ! command -v python; then
  echo "Python not found. Please install Python using your package manager or via PyEnv."
  exit 1
fi

requirements_file="requirements/main.txt"
venv_path=".venv"

# Parse command line arguments
download_models=false
for arg in "$@"; do
  case $arg in
    --download-models)
      download_models=true
      ;;
    *)
      ;;
  esac
done

if [[ ! -d "${venv_path}" ]]; then
  echo "Creating venv..."

  python -m venv "${venv_path}"
  source "${venv_path}/bin/activate"

  # Check if required packages are up-to-date
  pip install --upgrade -r "${requirements_file}"
fi
echo "Activating venv..."
source "${venv_path}/bin/activate"

# Download models if requested
if [ "$download_models" = true ]; then
  echo ""
  echo "Running model downloader..."
  python download_models.py
  download_exit_code=$?
  
  if [ $download_exit_code -eq 0 ]; then
    echo ""
    echo "Models are ready!"
  elif [ $download_exit_code -eq 2 ]; then
    echo ""
    echo "Note: Model download completed with warnings."
    echo "Some models may not have downloaded correctly."
  else
    echo ""
    echo "Error: Model download failed."
    echo "Please check the error messages above and try again."
    exit 1
  fi
  
  echo ""
  read -p "Press Enter to continue and start the application..."
  echo ""
fi

# Run the main script
echo "Starting RVC WebUI..."
python web.py --pycmd python
