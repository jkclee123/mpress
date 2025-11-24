"""Utility functions for mpress."""

import os
import shutil
from pathlib import Path
from typing import Optional


def atomic_replace(source: Path, destination: Path) -> None:
    """
    Atomically replace destination file with source file.

    This ensures that if the operation fails, the original file is preserved.
    The source file must be on the same filesystem as the destination (which is
    guaranteed if created in the same directory).

    Args:
        source: Path to the new file (temporary compressed file)
        destination: Path to the original file to be replaced

    Raises:
        OSError: If the replacement fails
    """
    # On Unix-like systems (including macOS), rename is atomic
    # First, ensure source exists
    if not source.exists():
        raise OSError(f"Source file does not exist: {source}")

    try:
        # Atomically replace destination with source file
        source.replace(destination)

    except Exception as e:
        # Clean up source file if it still exists
        if source.exists():
            try:
                source.unlink()
            except OSError:
                pass
        raise OSError(f"Failed to replace file {destination}: {e}") from e


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes
    """
    return file_path.stat().st_size

