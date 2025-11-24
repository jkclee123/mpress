# Implementation Plan: Media Compression Command Line Tool

**Feature Branch**: `001-compress-media`  
**Created**: 2025-01-27  
**Status**: Planning  
**Based on**: [spec.md](./spec.md)

## Tech Stack Recommendation

Since no tech stack preference was specified, the following recommendation is based on practical considerations for a macOS CLI tool:

### Recommended: Python 3.9+

**Rationale**:
- Excellent CLI libraries (`argparse`, `click`, or `typer`)
- Rich ecosystem for media processing:
  - **Images**: Pillow (PIL) for PNG/JPG/JPEG compression
  - **Videos**: FFmpeg (via subprocess or `ffmpeg-python`) for MOV/MP4/WebM
- Cross-platform compatibility (though macOS-focused)
- Can be compiled to standalone executable using PyInstaller (no Python installation required)
- Easy to install and distribute
- Good error handling capabilities
- Standard library support for file operations

**Alternative Options**:
- **Go**: Fast, single binary, but requires more setup for media processing
- **Rust**: Excellent performance, but steeper learning curve
- **Node.js**: Good ecosystem, but less common for CLI tools
- **Swift**: Native macOS, but video compression libraries are limited

### Dependencies

**Core**:
- Python 3.9+ (standard library: `argparse`, `sys`, `os`, `pathlib`)

**Media Processing**:
- `Pillow` (PIL) - Image compression (PNG, JPG, JPEG)
- `ffmpeg-python` or direct `ffmpeg` binary - Video compression (MOV, MP4, WebM)

**Distribution**:
- `PyInstaller` - Create standalone macOS executable (recommended for end users)
- `setuptools` - Create installable package with `setup.py` entry points (alternative for development)

**Note**: FFmpeg must be installed on the system (common on macOS via Homebrew). The PyInstaller executable will still require FFmpeg to be available on the user's system.

## Architecture Overview

### High-Level Design

```
mpress
├── CLI Interface (argparse/click)
│   ├── Parse command-line arguments
│   ├── Validate file paths
│   └── Route to appropriate compressor
├── File Handler
│   ├── Validate file existence
│   ├── Check file permissions
│   ├── Determine file type
│   └── Manage file replacement (atomic operations)
├── Image Compressor (PNG, JPG, JPEG)
│   ├── Use Pillow for compression
│   └── Apply fixed quality settings
└── Video Compressor (MOV, MP4, WebM)
    ├── Use FFmpeg for compression
    └── Apply fixed encoding settings
```

### Design Decisions

1. **Atomic File Replacement**: Compress to temporary file, then replace original atomically to prevent data loss
2. **Sequential Processing**: Process files one at a time (simpler error handling, predictable memory usage)
3. **Format Preservation**: Maintain original format (PNG→PNG, MP4→MP4)
4. **Fixed Compression Settings**: Hardcoded quality/bitrate settings for consistency
5. **Error Isolation**: Continue processing remaining files if one fails

## Implementation Tasks

### Phase 1: Project Setup & Core Infrastructure

#### Task 1.1: Initialize Project Structure
- [ ] Create project directory structure
- [ ] Set up Python virtual environment
- [ ] Create `requirements.txt` with dependencies
- [ ] Create `setup.py` or `pyproject.toml` for package installation
- [ ] Create `.gitignore` for Python projects
- [ ] Create basic `README.md` with installation instructions

#### Task 1.2: CLI Framework Setup
- [ ] Implement basic CLI entry point (`mpress` command)
- [ ] Set up argument parsing (accept multiple file paths)
- [ ] Implement basic help/usage output
- [ ] Handle no-arguments case (show usage)

**Acceptance**: `mpress --help` shows usage, `mpress` with no args shows error/usage

### Phase 2: File Handling & Validation

#### Task 2.1: File Validation Module
- [ ] Implement file existence checking
- [ ] Implement file permission checking (read/write)
- [ ] Implement file type detection (extension-based)
- [ ] Implement supported format validation
- [ ] Create error messages for missing/unsupported files

**Acceptance**: Tool correctly identifies missing files, unsupported formats, permission issues

#### Task 2.2: File Path Handling
- [ ] Support relative paths
- [ ] Support absolute paths
- [ ] Handle paths with spaces (quoted arguments)
- [ ] Normalize paths for macOS

**Acceptance**: Tool handles various path formats correctly

### Phase 3: Image Compression

#### Task 3.1: PNG Compression
- [ ] Implement PNG compression using Pillow
- [ ] Apply fixed compression level (optimize=True, compress_level=9)
- [ ] Preserve PNG format
- [ ] Handle compression errors gracefully

**Acceptance**: PNG files are compressed and replaced, format preserved

#### Task 3.2: JPEG/JPG Compression
- [ ] Implement JPEG compression using Pillow
- [ ] Apply fixed quality setting (quality=85 - good balance)
- [ ] Preserve JPEG format
- [ ] Handle compression errors gracefully

**Acceptance**: JPG/JPEG files are compressed and replaced, format preserved

#### Task 3.3: Image Compression Integration
- [ ] Create unified image compressor interface
- [ ] Route PNG/JPG/JPEG to appropriate compressor
- [ ] Implement atomic file replacement (temp file → original)
- [ ] Add error handling (preserve original on failure)

**Acceptance**: All image formats compress correctly, originals preserved on failure

### Phase 4: Video Compression

#### Task 4.1: FFmpeg Integration
- [ ] Check FFmpeg availability on system
- [ ] Implement FFmpeg subprocess wrapper
- [ ] Create error handling for FFmpeg failures
- [ ] Add helpful error messages if FFmpeg not found

**Acceptance**: Tool detects FFmpeg, handles missing FFmpeg gracefully

#### Task 4.2: Video Compression Implementation
- [ ] Implement MOV compression (H.264 codec, CRF 23)
- [ ] Implement MP4 compression (H.264 codec, CRF 23)
- [ ] Implement WebM compression (VP9 codec, CRF 30)
- [ ] Preserve original format
- [ ] Apply fixed quality settings (no user config)

**Acceptance**: All video formats compress correctly, format preserved

#### Task 4.3: Video Compression Integration
- [ ] Create unified video compressor interface
- [ ] Route MOV/MP4/WebM to appropriate compressor
- [ ] Implement atomic file replacement (temp file → original)
- [ ] Handle large files (streaming, memory-efficient)
- [ ] Add error handling (preserve original on failure)

**Acceptance**: All video formats compress correctly, originals preserved on failure

### Phase 5: Core Integration & Error Handling

#### Task 5.1: Main Processing Loop
- [ ] Implement sequential file processing
- [ ] Integrate file validation → compression → replacement flow
- [ ] Continue processing on individual file failures
- [ ] Collect and report errors per file
- [ ] Provide progress feedback (optional: file count)

**Acceptance**: Multiple files processed sequentially, errors don't stop processing

#### Task 5.2: Error Handling & Edge Cases
- [ ] Handle disk space exhaustion
- [ ] Handle already-compressed files (skip or recompress)
- [ ] Handle corrupted input files
- [ ] Handle very large files (memory management)
- [ ] Preserve original files on any failure

**Acceptance**: All edge cases handled gracefully, no data loss

#### Task 5.3: User Feedback
- [ ] Implement clear error messages
- [ ] Provide success confirmation (optional)
- [ ] Show which files failed and why
- [ ] Exit codes (0 = success, 1 = errors)

**Acceptance**: Users understand what happened with each file

### Phase 6: Testing & Validation

#### Task 6.1: Unit Tests
- [ ] Test file validation logic
- [ ] Test image compression functions
- [ ] Test video compression functions (mocked FFmpeg)
- [ ] Test error handling paths
- [ ] Test file replacement logic

**Acceptance**: Core logic covered by unit tests

#### Task 6.2: Integration Tests
- [ ] Test end-to-end with sample files
- [ ] Test all supported formats
- [ ] Test multiple file processing
- [ ] Test error scenarios (missing files, permissions, etc.)
- [ ] Test with files from `work/` directory

**Acceptance**: All user scenarios from spec work correctly

#### Task 6.3: Manual Testing
- [ ] Test with real media files (PNG, JPG, MOV, MP4, WebM)
- [ ] Verify file size reduction
- [ ] Verify quality preservation (visual inspection)
- [ ] Test edge cases manually
- [ ] Test on macOS

**Acceptance**: Tool works reliably with real-world files

### Phase 7: Distribution & Documentation

#### Task 7.1: Standalone Executable (PyInstaller) - Recommended
- [ ] Install PyInstaller: `pip install pyinstaller`
- [ ] Create PyInstaller spec file (`mpress.spec`) for configuration
- [ ] Build standalone executable: `pyinstaller --onefile --name mpress mpress/cli.py`
- [ ] Test executable works: `./dist/mpress 2.png cap.mov`
- [ ] Create installation script to copy executable to `/usr/local/bin` or user's PATH
- [ ] Test that `mpress` command works from any directory after installation
- [ ] Document FFmpeg installation requirement (still needed even with standalone executable)

**Acceptance**: Users can run `mpress 2.png cap.mov` directly without Python installed

#### Task 7.2: Alternative Installation (setup.py) - For Development
- [ ] Create `setup.py` with entry_points configuration
- [ ] Define console script: `entry_points={'console_scripts': ['mpress=mpress.cli:main']}`
- [ ] Test installation: `pip install -e .`
- [ ] Verify `mpress` command is available in PATH after installation
- [ ] Document installation instructions

**Acceptance**: Developers can install tool via pip and use `mpress` command

#### Task 7.3: Documentation
- [ ] Update README with usage examples (`mpress 2.png cap.mov`)
- [ ] Document supported formats
- [ ] Document requirements (FFmpeg)
- [ ] Add installation instructions for both methods
- [ ] Add troubleshooting section
- [ ] Include example commands from spec

**Acceptance**: Users can understand and use the tool

#### Task 7.2: Documentation
- [ ] Update README with usage examples
- [ ] Document supported formats
- [ ] Document requirements (Python, FFmpeg)
- [ ] Add troubleshooting section

**Acceptance**: Users can understand and use the tool

## Compression Settings (Fixed)

### Images
- **PNG**: `optimize=True`, `compress_level=9` (maximum compression)
- **JPEG/JPG**: `quality=85` (good balance between size and quality)

### Videos
- **MOV/MP4**: H.264 codec, CRF 23 (good quality, reasonable compression)
- **WebM**: VP9 codec, CRF 30 (good quality, reasonable compression)

**Note**: These settings provide a balance between file size reduction and quality preservation. They are hardcoded and not user-configurable per requirements.

## File Structure

```
mpress/
├── mpress/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point and argument parsing
│   ├── file_handler.py     # File validation and path handling
│   ├── image_compressor.py # PNG/JPG/JPEG compression
│   ├── video_compressor.py # MOV/MP4/WebM compression
│   └── utils.py            # Utility functions (atomic replace, etc.)
├── tests/
│   ├── __init__.py
│   ├── test_file_handler.py
│   ├── test_image_compressor.py
│   └── test_video_compressor.py
├── requirements.txt
├── setup.py
├── mpress.spec              # PyInstaller configuration (optional)
├── README.md
└── .gitignore
```

## Risk Assessment

### Technical Risks

1. **FFmpeg Dependency**: Users must have FFmpeg installed
   - **Mitigation**: Clear error message with installation instructions
   - **Impact**: Medium - affects video compression only

2. **Large File Handling**: Very large videos may cause memory issues
   - **Mitigation**: Use FFmpeg streaming, process files sequentially
   - **Impact**: Low - FFmpeg handles this well

3. **Quality Loss**: Fixed compression may not suit all use cases
   - **Mitigation**: Use conservative quality settings (per requirements)
   - **Impact**: Low - acceptable per spec (no user config)

4. **File Corruption**: Compression failure could corrupt files
   - **Mitigation**: Atomic file replacement, preserve original on failure
   - **Impact**: High - must be handled correctly

### Project Risks

1. **Time Estimation**: Video compression can be slow for large files
   - **Mitigation**: Set expectations, consider progress indicators
   - **Impact**: Low - acceptable for CLI tool

## Success Metrics

- [ ] All functional requirements (FR-001 through FR-017) implemented
- [ ] All acceptance scenarios from User Stories pass
- [ ] Edge cases handled gracefully
- [ ] Tool compresses 95%+ of valid files successfully (SC-004)
- [ ] No data loss (original preserved on failure)
- [ ] Clear error messages for all failure modes
- [ ] Works on macOS as specified

## Next Steps

1. Review and approve this plan
2. Set up project structure (Task 1.1)
3. Begin implementation with Phase 1
4. Iterate through phases, testing as we go
5. Final validation against spec requirements

## Distribution Options

### Option 1: Standalone Executable (PyInstaller) - **Recommended**

Creates a single binary file that can be run directly as `mpress 2.png cap.mov` without requiring Python to be installed.

**Pros**:
- No Python installation required for end users
- Single file distribution
- Works exactly like a native macOS command-line tool
- Can be placed in `/usr/local/bin` or any PATH directory

**Cons**:
- Larger file size (includes Python runtime and dependencies)
- Still requires FFmpeg to be installed on the system
- Must be rebuilt for different architectures (Intel vs Apple Silicon)

**Build Command**:
```bash
pyinstaller --onefile --name mpress mpress/cli.py
```

**Installation**:
```bash
# Copy to a directory in PATH
cp dist/mpress /usr/local/bin/mpress
chmod +x /usr/local/bin/mpress
```

### Option 2: Python Package (setup.py)

Installs as a Python package that creates a `mpress` command-line script.

**Pros**:
- Smaller distribution size
- Easier for development and testing
- Standard Python packaging

**Cons**:
- Requires Python to be installed
- Requires pip installation step

**Installation**:
```bash
pip install -e .
# Then use: mpress 2.png cap.mov
```

## Notes

- This plan assumes Python as the implementation language. If a different language is preferred, the structure can be adapted.
- **PyInstaller is recommended** for creating a standalone executable that works as `mpress 2.png cap.mov` without Python installation.
- FFmpeg installation is a prerequisite for video compression (even with PyInstaller executable). Consider documenting this clearly.
- Compression settings are fixed per requirements - no user configuration needed.
- The tool should be simple and focused - avoid feature creep beyond the spec.

