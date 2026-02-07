# Release Notes for RVC-MacOS

## Version 1.0.0 (TBD)

### Features
- Initial release of standalone macOS application
- Native .app bundle using py2app
- DMG installer for easy distribution
- Support for Apple Silicon (M1/M2/M3) and Intel Macs
- Automatic model downloading
- Web-based user interface
- Voice conversion with high-quality results
- Training capabilities for custom voice models
- MPS (Metal Performance Shaders) acceleration for Apple Silicon
- RMVPE pitch extraction algorithm

### Build System
- Automated build scripts (build_app.sh, create_dmg.sh)
- GitHub Actions workflow for automated releases
- Comprehensive packaging documentation

### Requirements
- macOS 12.0 or later
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

### Known Issues
- App is not code-signed (users may need to allow in Security & Privacy settings)
- First launch may be slow as resources are unpacked

### Credits
Based on [RVC-WebUI-MacOS](https://github.com/audiohacking/RVC-WebUI-MacOS)
Original project: [Retrieval-based-Voice-Conversion-WebUI](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI)
