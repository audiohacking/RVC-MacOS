# Release v0.0.1 - Instructions and Testing Guide

## Current Status: ✅ READY TO RELEASE

All preparation for the v0.0.1 test release is complete. The code is ready, the tag is created locally, and the GitHub Actions workflow is configured.

## What Was Done

### 1. Version Updates
- `VERSION` file: 1.0.0 → 0.0.1
- `setup.py`: All version references updated to 0.0.1
  - CFBundleVersion: 0.0.1
  - CFBundleShortVersionString: 0.0.1
  - setup() version: 0.0.1

### 2. CHANGELOG.md Updated
- Added detailed v0.0.1 release notes
- Marked as "Test Release"
- Documented purpose: validate build system
- Listed all features and security fixes
- Added testing notes section

### 3. GitHub Actions Workflow Fixed
- **CRITICAL FIX**: Removed model download step from build
- Reason: Models should NOT be pre-bundled (design decision)
- Result: DMG will be ~500MB instead of ~3GB
- Added clear comment explaining the decision

### 4. Git Tag Created
- Tag: `v0.0.1`
- Type: Lightweight tag
- Target: Latest commit (0574836)
- Status: Created locally, ready to push

## How to Trigger the Release

### Option 1: Push the Tag (Recommended)

```bash
cd /home/runner/work/RVC-MacOS/RVC-MacOS
git push origin v0.0.1
```

This will immediately trigger the GitHub Actions workflow.

### Option 2: Create Release via GitHub Web UI

1. Go to: https://github.com/audiohacking/RVC-MacOS/releases/new
2. Fill in:
   - **Tag**: `v0.0.1`
   - **Target**: `copilot/generate-rvc-macos-app` branch
   - **Release title**: `Test Release v0.0.1`
   - **Description**: Copy from `CHANGELOG.md` (v0.0.1 section)
   - **Options**: Check "This is a pre-release"
3. Click "Publish release"

This will also trigger the workflow.

## What Will Happen

### GitHub Actions Workflow Steps

1. **Trigger**: When tag `v0.0.1` is pushed
2. **Runner**: macOS-latest (Apple Silicon or Intel)
3. **Duration**: 20-40 minutes estimated

#### Workflow Steps:
```
1. Checkout code
2. Set up Python 3.10
3. Install system dependencies (brew install portaudio)
4. Create virtual environment
5. Install pip packages from requirements/gui.txt
   - PyTorch 2.6.0+
   - Gradio, Flask, FastAPI
   - Audio processing libraries
   - ML frameworks
6. Install py2app
7. Build .app bundle (python setup.py py2app)
8. Create DMG installer (./create_dmg.sh)
9. Extract version from tag (0.0.1)
10. Create GitHub Release
11. Upload DMG to release
12. Upload artifacts (DMG + .app)
```

### Expected Outputs

**GitHub Release:**
- URL: https://github.com/audiohacking/RVC-MacOS/releases/tag/v0.0.1
- Assets: `RVC-MacOS-Installer.dmg` (~500MB)
- Type: Pre-release
- Auto-generated release notes

**Artifacts (30-day retention):**
- Name: `RVC-MacOS-0.0.1`
- Contents:
  - `RVC-MacOS-Installer.dmg`
  - `RVC-MacOS.app/` (directory)

### Build Time Breakdown

- **Python dependencies install**: ~10-15 minutes
  - PyTorch and related packages are large
  - macOS-specific builds need compilation
- **py2app build**: ~5-10 minutes
  - Bundles Python runtime
  - Includes all libraries
  - Creates .app structure
- **DMG creation**: ~1-2 minutes
  - Creates disk image
  - Adds Applications symlink
- **Upload**: ~2-5 minutes
  - Depends on file size and network speed

**Total**: 20-40 minutes

## How to Monitor the Build

### 1. GitHub Actions Page
https://github.com/audiohacking/RVC-MacOS/actions

You'll see:
- Workflow name: "Build macOS App"
- Triggered by: "Tag v0.0.1"
- Status: Running → Success/Failure

### 2. Live Log Viewing
Click on the running workflow to see:
- Each step's progress
- Real-time console output
- Any errors or warnings

### 3. Key Things to Watch For

**✅ Good Signs:**
- Python 3.10 installed successfully
- All pip packages installed without errors
- py2app completes without warnings
- DMG file created (should be ~500MB)
- Release created successfully

**❌ Potential Issues:**
- Dependency conflicts (check requirements files)
- py2app errors (check setup.py configuration)
- DMG creation fails (check create_dmg.sh)
- Disk space issues on runner
- Network timeouts during package download

## If the Build Fails

### Step 1: Review the Logs
1. Go to failed workflow run
2. Click on the failed step
3. Read the error messages carefully
4. Note the exact error and step that failed

### Step 2: Common Issues and Fixes

**Issue: Dependency installation fails**
```
Fix: Update requirements/gui.txt
- Check for conflicting version requirements
- Test locally if possible
```

**Issue: py2app build fails**
```
Fix: Update setup.py
- Check packages list
- Verify includes are correct
- Check for missing dependencies
```

**Issue: DMG creation fails**
```
Fix: Check create_dmg.sh
- Verify hdiutil commands
- Check disk space
- Verify .app exists before DMG creation
```

**Issue: Release creation fails**
```
Fix: Check workflow permissions
- Ensure GITHUB_TOKEN has release permissions
- Verify tag format matches 'v*'
```

### Step 3: Delete the Failed Release

**Via GitHub UI:**
1. Go to: https://github.com/audiohacking/RVC-MacOS/releases
2. Find v0.0.1 release
3. Click "Delete"

**Via Git:**
```bash
# Delete remote tag
git push origin :refs/tags/v0.0.1

# Delete local tag
git tag -d v0.0.1
```

### Step 4: Fix the Issue
1. Make the necessary code changes
2. Commit and push to the branch
3. Recreate the tag:
   ```bash
   git tag v0.0.1
   git push origin v0.0.1
   ```

### Step 5: Retry
The workflow will automatically run again when you push the new tag.

## Testing the Release

Once the build succeeds and the release is created:

### 1. Download the DMG
```
https://github.com/audiohacking/RVC-MacOS/releases/download/v0.0.1/RVC-MacOS-Installer.dmg
```

### 2. Verify DMG Size
- Expected: ~500MB
- If much larger (>2GB): Models were accidentally included
- If much smaller (<100MB): Dependencies might be missing

### 3. Verify DMG Contents (Optional)
```bash
# Mount the DMG
hdiutil attach RVC-MacOS-Installer.dmg

# Check contents
ls -lh /Volumes/RVC-MacOS\ 0.0.1/

# Should see:
# - RVC-MacOS.app
# - Applications (symlink)

# Unmount
hdiutil detach /Volumes/RVC-MacOS\ 0.0.1/
```

### 4. Verify .app Bundle (Optional)
```bash
# Check bundle size
du -sh /Volumes/RVC-MacOS\ 0.0.1/RVC-MacOS.app

# Should be ~500MB (without models)

# Check if Python is bundled
ls -la /Volumes/RVC-MacOS\ 0.0.1/RVC-MacOS.app/Contents/MacOS/
ls -la /Volumes/RVC-MacOS\ 0.0.1/RVC-MacOS.app/Contents/Resources/lib/
```

## Success Criteria

The v0.0.1 release is successful if:

- ✅ GitHub Actions workflow completes without errors
- ✅ Release is created at the correct URL
- ✅ DMG file is ~500MB (not 2-3GB)
- ✅ DMG contains RVC-MacOS.app
- ✅ App bundle contains Python and all dependencies
- ✅ No models are pre-bundled in the app
- ✅ Artifacts are uploaded successfully

## Next Steps After Success

1. **Announce** the test release
2. **Test** the app on a real macOS system:
   - Install from DMG
   - Launch the app
   - Verify model download works
   - Test voice conversion functionality
3. **Gather feedback** on:
   - Installation process
   - First-launch experience
   - Model download time
   - App performance
4. **Document any issues** found during testing
5. **Plan** for v0.0.2 or v1.0.0 based on results

## Quick Reference

### Important URLs
- Repository: https://github.com/audiohacking/RVC-MacOS
- Actions: https://github.com/audiohacking/RVC-MacOS/actions
- Releases: https://github.com/audiohacking/RVC-MacOS/releases
- This Release: https://github.com/audiohacking/RVC-MacOS/releases/tag/v0.0.1

### Important Files
- Workflow: `.github/workflows/build-macos.yml`
- Version: `VERSION`
- Setup: `setup.py`
- Changelog: `CHANGELOG.md`
- Build script: `build_app.sh`
- DMG script: `create_dmg.sh`

### Current State
- Branch: `copilot/generate-rvc-macos-app`
- Latest commit: `0574836`
- Tag: `v0.0.1` (created locally)
- Status: Ready to push tag

---

**Ready to release!** Push the tag to start the build. 🚀
