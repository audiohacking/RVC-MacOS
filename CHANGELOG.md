# Release Notes for RVC-MacOS

## Version 0.0.1 (2026-02-07) - Test Release

### Purpose
Initial test release to validate the build system and GitHub Actions workflow.

### Features
- Initial release of standalone macOS application
- Native .app bundle using py2app
- DMG installer for easy distribution
- Support for Apple Silicon (M1/M2/M3) and Intel Macs
- Automatic model downloading on first launch
- Web-based user interface
- Voice conversion with high-quality results
- Training capabilities for custom voice models
- MPS (Metal Performance Shaders) acceleration for Apple Silicon
- RMVPE pitch extraction algorithm

### Security
- PyTorch updated to 2.6.0+ (fixes multiple CVEs)
- Fixed heap buffer overflow vulnerability
- Fixed use-after-free vulnerability
- Fixed torch.load RCE vulnerability

### Build System
- Automated build scripts (build_app.sh, create_dmg.sh)
- GitHub Actions workflow for automated releases
- Comprehensive packaging documentation
- All Python dependencies bundled (users install nothing)

### Requirements
- macOS 12.0 or later
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space (for models and temp files)

### Known Issues
- App is not code-signed (users may need to allow in Security & Privacy settings)
- First launch takes 5-10 minutes to download AI models (~1.5GB)

### Testing Notes
This is a test release to validate:
- GitHub Actions build process
- py2app packaging
- Model download during build
- DMG creation
- Automatic release generation

### Credits
Based on [RVC-WebUI-MacOS](https://github.com/audiohacking/RVC-WebUI-MacOS)
Original project: [Retrieval-based-Voice-Conversion-WebUI](https://github.com/fumiama/Retrieval-based-Voice-Conversion-WebUI)

---

## Version 1.0.0 (TBD) - Future Release

Planned for stable production release after successful testing of 0.0.1.
