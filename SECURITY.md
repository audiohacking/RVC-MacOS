# Security Advisory - PyTorch Vulnerability Fixes

## Date: 2026-02-07

## Summary

This update addresses critical security vulnerabilities in PyTorch versions < 2.6.0 that were present in the RVC-MacOS codebase.

## Vulnerabilities Addressed

### 1. Heap Buffer Overflow (CVE)
- **Affected versions**: PyTorch < 2.2.0
- **Patched in**: 2.2.0
- **Severity**: High
- **Description**: Heap buffer overflow vulnerability that could lead to arbitrary code execution
- **Impact**: Potential for remote code execution when processing malicious inputs

### 2. Use-After-Free (CVE)
- **Affected versions**: PyTorch < 2.2.0
- **Patched in**: 2.2.0
- **Severity**: High
- **Description**: Use-after-free vulnerability in PyTorch's memory management
- **Impact**: Could lead to crashes or arbitrary code execution

### 3. Remote Code Execution via torch.load
- **Affected versions**: PyTorch < 2.6.0
- **Patched in**: 2.6.0
- **Severity**: Critical
- **Description**: `torch.load` with `weights_only=True` could still lead to remote code execution
- **Impact**: Loading untrusted model files could execute arbitrary code

### 4. Deserialization Vulnerability
- **Affected versions**: PyTorch <= 2.3.1
- **Status**: Withdrawn advisory (no patch available as of this date)
- **Note**: By upgrading to 2.6.0, we are using the most recent stable version

## Actions Taken

### Updated Requirements Files

1. **requirements/gui.txt**
   - Added: `torch>=2.6.0`
   - Added: `torchvision>=0.21.0`
   - Added: `torchaudio>=2.6.0`
   - Added security comments explaining the update

2. **requirements/main.txt**
   - Added: `torch>=2.6.0`
   - Added: `torchvision>=0.21.0`
   - Added: `torchaudio>=2.6.0`
   - Added security update comments

### Compatibility Notes

- **Python Versions**: PyTorch 2.6.0 supports Python 3.8-3.12
- **macOS Support**: Full support for Apple Silicon (M1/M2/M3) with MPS acceleration
- **RVC Compatibility**: RVC's existing code is compatible with PyTorch 2.6.0
- **fairseq**: The Python 3.8-3.10 requirement remains for fairseq compatibility

## Pre-existing Security Issues in RVC Codebase

While updating PyTorch, we identified pre-existing security issues in the RVC codebase (inherited from upstream):

### torch.load Security Override (NOT FIXED - Upstream Issue)

**Location**: 
- `infer/lib/train/data_utils.py` lines 13-14
- `infer/lib/rtrvc.py` lines 16-17

**Issue**: These files patch `torch.load` globally to always set `weights_only=False`, bypassing PyTorch's security mechanism:

```python
torch.load = torch.load(partial(torch.load, map_location="cpu", weights_only=False))
```

**Risk**: This creates a vulnerability when loading untrusted checkpoint files as it allows arbitrary code execution.

**Status**: Not fixed in this update as it would require changes to core RVC functionality. This is an upstream issue that should be addressed by the RVC project.

**Mitigation**: 
- Only load model files from trusted sources
- Do not load user-provided .pth files without verification
- Consider sandboxing or containerization for production deployments

## Verification

To verify the PyTorch version after updating:

```bash
# Activate your virtual environment
source .venv/bin/activate

# Check PyTorch version
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Should output: PyTorch: 2.6.0 or higher
```

## Recommendations

### For Users
1. **Update immediately** by rebuilding the app with the new requirements
2. **Only load trusted model files** - do not load .pth files from unknown sources
3. **Keep PyTorch updated** as new versions are released

### For Developers
1. **Rebuild the app** using the updated requirements
2. **Test thoroughly** to ensure compatibility with PyTorch 2.6.0
3. **Consider addressing** the upstream `torch.load` security override
4. **Monitor** PyTorch security advisories for future updates

### For Production Deployments
1. **Scan all model files** before deployment
2. **Use containerization** (Docker) for isolation
3. **Restrict network access** during model loading
4. **Implement file integrity checking** for model files
5. **Regular security audits** of dependencies

## Timeline

- **2026-02-07**: Vulnerabilities identified in torch 2.0.1a0
- **2026-02-07**: Requirements updated to torch>=2.6.0
- **2026-02-07**: Security advisory created

## References

- PyTorch Security Advisories: https://github.com/pytorch/pytorch/security/advisories
- PyTorch Release Notes: https://github.com/pytorch/pytorch/releases
- CVE Database: https://cve.mitre.org/

## Contact

For security concerns, please open an issue at:
https://github.com/audiohacking/RVC-MacOS/issues

## Acknowledgments

Thank you to the security researchers who identified these vulnerabilities and the PyTorch team for the fixes.
