# Implementation Tasks

**Feature**: Media Compression Command Line Tool (`001-compress-media`)
**Based on**: [plan.md](../plan.md)

## Phase 1: Project Setup & Core Infrastructure

### Task 1.1: Initialize Project Structure
- [ ] Create project directory structure
- [ ] Set up Python virtual environment
- [ ] Create `requirements.txt` with dependencies
- [ ] Create `setup.py` or `pyproject.toml` for package installation
- [ ] Create `.gitignore` for Python projects
- [ ] Create basic `README.md` with installation instructions

### Task 1.2: CLI Framework Setup
- [ ] Implement basic CLI entry point (`mpress` command)
- [ ] Set up argument parsing (accept multiple file paths)
- [ ] Implement basic help/usage output
- [ ] Handle no-arguments case (show usage)

**Acceptance**: `mpress --help` shows usage, `mpress` with no args shows error/usage

## Phase 2: File Handling & Validation

### Task 2.1: File Validation Module
- [ ] Implement file existence checking
- [ ] Implement file permission checking (read/write)
- [ ] Implement file type detection (extension-based)
- [ ] Implement supported format validation
- [ ] Create error messages for missing/unsupported files

**Acceptance**: Tool correctly identifies missing files, unsupported formats, permission issues

### Task 2.2: File Path Handling
- [ ] Support relative paths
- [ ] Support absolute paths
- [ ] Handle paths with spaces (quoted arguments)
- [ ] Normalize paths for macOS

**Acceptance**: Tool handles various path formats correctly

## Phase 3: Image Compression

### Task 3.1: PNG Compression
- [ ] Implement PNG compression using Pillow
- [ ] Apply fixed compression level (optimize=True, compress_level=9)
- [ ] Preserve PNG format
- [ ] Handle compression errors gracefully

**Acceptance**: PNG files are compressed and replaced, format preserved

### Task 3.2: JPEG/JPG Compression
- [ ] Implement JPEG compression using Pillow
- [ ] Apply fixed quality setting (quality=85 - good balance)
- [ ] Preserve JPEG format
- [ ] Handle compression errors gracefully

**Acceptance**: JPG/JPEG files are compressed and replaced, format preserved

### Task 3.3: Image Compression Integration
- [ ] Create unified image compressor interface
- [ ] Route PNG/JPG/JPEG to appropriate compressor
- [ ] Implement atomic file replacement (temp file → original)
- [ ] Add error handling (preserve original on failure)

**Acceptance**: All image formats compress correctly, originals preserved on failure

## Phase 4: Video Compression

### Task 4.1: FFmpeg Integration
- [ ] Check FFmpeg availability on system
- [ ] Implement FFmpeg subprocess wrapper
- [ ] Create error handling for FFmpeg failures
- [ ] Add helpful error messages if FFmpeg not found

**Acceptance**: Tool detects FFmpeg, handles missing FFmpeg gracefully

### Task 4.2: Video Compression Implementation
- [ ] Implement MOV compression (H.264 codec, CRF 23)
- [ ] Implement MP4 compression (H.264 codec, CRF 23)
- [ ] Implement WebM compression (VP9 codec, CRF 30)
- [ ] Preserve original format
- [ ] Apply fixed quality settings (no user config)

**Acceptance**: All video formats compress correctly, format preserved

### Task 4.3: Video Compression Integration
- [ ] Create unified video compressor interface
- [ ] Route MOV/MP4/WebM to appropriate compressor
- [ ] Implement atomic file replacement (temp file → original)
- [ ] Handle large files (streaming, memory-efficient)
- [ ] Add error handling (preserve original on failure)

**Acceptance**: All video formats compress correctly, originals preserved on failure

## Phase 5: Core Integration & Error Handling

### Task 5.1: Main Processing Loop
- [ ] Implement sequential file processing
- [ ] Integrate file validation → compression → replacement flow
- [ ] Continue processing on individual file failures
- [ ] Collect and report errors per file
- [ ] Provide progress feedback (optional: file count)

**Acceptance**: Multiple files processed sequentially, errors don't stop processing

### Task 5.2: Error Handling & Edge Cases
- [ ] Handle disk space exhaustion
- [ ] Handle already-compressed files (skip or recompress)
- [ ] Handle corrupted input files
- [ ] Handle very large files (memory management)
- [ ] Preserve original files on any failure

**Acceptance**: All edge cases handled gracefully, no data loss

### Task 5.3: User Feedback
- [ ] Implement clear error messages
- [ ] Provide success confirmation (optional)
- [ ] Show which files failed and why
- [ ] Exit codes (0 = success, 1 = errors)

**Acceptance**: Users understand what happened with each file

## Phase 6: Testing & Validation

### Task 6.1: Unit Tests
- [ ] Test file validation logic
- [ ] Test image compression functions
- [ ] Test video compression functions (mocked FFmpeg)
- [ ] Test error handling paths
- [ ] Test file replacement logic

**Acceptance**: Core logic covered by unit tests

### Task 6.2: Integration Tests
- [ ] Test end-to-end with sample files
- [ ] Test all supported formats
- [ ] Test multiple file processing
- [ ] Test error scenarios (missing files, permissions, etc.)
- [ ] Test with files from `work/` directory

**Acceptance**: All user scenarios from spec work correctly

### Task 6.3: Manual Testing
- [ ] Test with real media files (PNG, JPG, MOV, MP4, WebM)
- [ ] Verify file size reduction
- [ ] Verify quality preservation (visual inspection)
- [ ] Test edge cases manually
- [ ] Test on macOS

**Acceptance**: Tool works reliably with real-world files

## Phase 7: Distribution & Documentation

### Task 7.1: Standalone Executable (PyInstaller)
- [ ] Install PyInstaller: `pip install pyinstaller`
- [ ] Create PyInstaller spec file (`mpress.spec`) for configuration
- [ ] Build standalone executable: `pyinstaller --onefile --name mpress mpress/cli.py`
- [ ] Test executable works: `./dist/mpress 2.png cap.mov`
- [ ] Create installation script to copy executable to `/usr/local/bin` or user's PATH
- [ ] Test that `mpress` command works from any directory after installation
- [ ] Document FFmpeg installation requirement

**Acceptance**: Users can run `mpress 2.png cap.mov` directly without Python installed

### Task 7.2: Alternative Installation (setup.py)
- [ ] Create `setup.py` with entry_points configuration
- [ ] Define console script: `entry_points={'console_scripts': ['mpress=mpress.cli:main']}`
- [ ] Test installation: `pip install -e .`
- [ ] Verify `mpress` command is available in PATH after installation
- [ ] Document installation instructions

**Acceptance**: Developers can install tool via pip and use `mpress` command

### Task 7.3: Documentation
- [ ] Update README with usage examples
- [ ] Document supported formats
- [ ] Document requirements (Python, FFmpeg)
- [ ] Add installation instructions for both methods
- [ ] Add troubleshooting section

**Acceptance**: Users can understand and use the tool

