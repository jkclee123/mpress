"""File validation and path handling for mpress."""

import os
from pathlib import Path
from typing import List, Tuple


# Supported file formats
SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg"}
SUPPORTED_VIDEO_FORMATS = {".mov", ".mp4", ".webm"}
SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | SUPPORTED_VIDEO_FORMATS


class FileValidationError(Exception):
    """Exception raised when file validation fails."""

    pass


def validate_file(file_path: str) -> Tuple[Path, str]:
    """
    Validate a file path and return the Path object and file type.

    Args:
        file_path: String path to the file

    Returns:
        Tuple of (Path object, file_type) where file_type is 'image' or 'video'

    Raises:
        FileValidationError: If file doesn't exist, can't be read, or format is unsupported
    """
    path = Path(file_path).resolve()

    # Check if file exists
    if not path.exists():
        raise FileValidationError(f"File not found: {file_path}")

    # Check if it's a file (not a directory)
    if not path.is_file():
        raise FileValidationError(f"Not a file: {file_path}")

    # Check read permissions
    if not os.access(path, os.R_OK):
        raise FileValidationError(f"Cannot read file: {file_path}")

    # Check write permissions (needed to replace the file)
    if not os.access(path, os.W_OK):
        raise FileValidationError(f"Cannot write to file: {file_path}")

    # Get file extension
    extension = path.suffix.lower()

    # Validate format
    if extension not in SUPPORTED_FORMATS:
        raise FileValidationError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )

    # Determine file type
    if extension in SUPPORTED_IMAGE_FORMATS:
        file_type = "image"
    elif extension in SUPPORTED_VIDEO_FORMATS:
        file_type = "video"
    else:
        # This shouldn't happen, but handle it anyway
        raise FileValidationError(f"Unknown file type for extension: {extension}")

    return path, file_type


def normalize_path(file_path: str) -> Path:
    """
    Normalize a file path for macOS.

    Args:
        file_path: String path to normalize

    Returns:
        Normalized Path object
    """
    return Path(file_path).expanduser().resolve()


def validate_files(file_paths: List[str]) -> List[Tuple[Path, str, str]]:
    """
    Validate multiple file paths.

    Args:
        file_paths: List of file path strings

    Returns:
        List of tuples: (Path object, file_type, original_path)
        Files that fail validation are skipped (errors should be handled by caller)

    Note:
        This function collects validation errors but doesn't raise them.
        The caller should handle errors appropriately.
    """
    validated_files = []
    for file_path in file_paths:
        try:
            normalized_path = normalize_path(file_path)
            path, file_type = validate_file(str(normalized_path))
            validated_files.append((path, file_type, file_path))
        except FileValidationError:
            # Skip invalid files - errors will be reported by caller
            pass

    return validated_files

