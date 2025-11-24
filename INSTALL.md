# Installing the mpress Executable

## Executable Location

The standalone executable has been built and is located at:
```
dist/mpress
```

## Installation Options

### Option 1: Install to `/usr/local/bin` (Recommended)

This makes `mpress` available system-wide for all users:

```bash
# Copy the executable
sudo cp dist/mpress /usr/local/bin/mpress

# Make it executable (should already be, but ensure it)
sudo chmod +x /usr/local/bin/mpress

# Verify installation
which mpress
mpress --help
```

**Note**: Requires administrator privileges (sudo).

### Option 2: Install to `~/bin` (User-specific)

This makes `mpress` available only for your user account:

```bash
# Create ~/bin directory if it doesn't exist
mkdir -p ~/bin

# Copy the executable
cp dist/mpress ~/bin/mpress

# Make it executable
chmod +x ~/bin/mpress

# Add ~/bin to your PATH (if not already there)
# Add this line to your ~/.zshrc or ~/.bash_profile:
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# Reload your shell configuration
source ~/.zshrc

# Verify installation
which mpress
mpress --help
```

### Option 3: Use from Current Location

You can use the executable directly without installing:

```bash
# Run from the dist directory
./dist/mpress --help
./dist/mpress image.png video.mp4

# Or add the dist directory to your PATH temporarily
export PATH="$PWD/dist:$PATH"
mpress --help
```

## Testing the Installation

After installation, test the executable:

```bash
# Test help command
mpress --help

# Test with a file (use a test file first!)
mpress test.png
```

## Important Notes

1. **FFmpeg Required**: The executable still requires FFmpeg to be installed on your system for video compression. Install it with:
   ```bash
   brew install ffmpeg
   ```

2. **Architecture**: This executable was built for Apple Silicon (ARM64). If you're on an Intel Mac, you'll need to rebuild it.

3. **File Permissions**: Make sure the executable has execute permissions:
   ```bash
   chmod +x /usr/local/bin/mpress  # or wherever you installed it
   ```

4. **Security**: macOS may show a security warning the first time you run the executable. You may need to:
   - Right-click the executable → Open → Click "Open" in the dialog
   - Or go to System Settings → Privacy & Security → Allow the application

## Troubleshooting

### "Command not found"
- Make sure the installation directory is in your PATH
- Try `echo $PATH` to verify
- Restart your terminal after adding to PATH

### "Permission denied"
- Make sure the file has execute permissions: `chmod +x mpress`
- If installing to `/usr/local/bin`, use `sudo`

### "FFmpeg not found" (for video files)
- Install FFmpeg: `brew install ffmpeg`
- Verify installation: `which ffmpeg`

