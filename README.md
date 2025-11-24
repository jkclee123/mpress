# mpress

A command-line tool for compressing media files on macOS. Compresses PNG, JPG, JPEG, MOV, MP4, and WebM files, replacing the originals with compressed versions.

## Features

- Compress images (PNG, JPG, JPEG) using optimized settings
- Compress videos (MOV, MP4, WebM) using FFmpeg
- Process single or multiple files in one command
- Automatic file replacement (original files are replaced with compressed versions)
- Fixed compression settings for consistent results

## Requirements

- Python 3.9 or higher
- FFmpeg (required for video compression)
  - Install via Homebrew: `brew install ffmpeg`

## Installation

```bash
# Install dependencies
pip install -e .

# The mpress command will be available in your PATH
```

## Building Standalone Executable

You can build a standalone executable that doesn't require Python to be installed on the target machine (though FFmpeg is still required for video compression).

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller mpress.spec
   ```

   The executable will be generated at `dist/mpress`.

3. Install the executable system-wide:
   ```bash
   sudo cp dist/mpress /usr/local/bin/mpress
   sudo chmod +x /usr/local/bin/mpress
   ```

   After installation, the `mpress` command will be available system-wide.

## Usage

```bash
# Compress a single file
mpress image.png

# Compress multiple files
mpress 2.png cap.mov

# Compress files with spaces in names (use quotes)
mpress "My Photo.jpg" "My Video.mp4"
```

## Supported Formats

- **Images**: PNG, JPG, JPEG
- **Videos**: MOV, MP4, WebM

## Compression Settings

The tool uses fixed compression settings optimized for quality and file size:

- **PNG**: Maximum compression (optimize=True, compress_level=9)
- **JPEG/JPG**: Quality 85 (good balance between size and quality)
- **MOV/MP4**: H.264 codec, CRF 23
- **WebM**: VP9 codec, CRF 30

## Error Handling

- If a file cannot be compressed, the original file is preserved
- Error messages are displayed for missing files or unsupported formats
- Processing continues even if individual files fail

## License

MIT

