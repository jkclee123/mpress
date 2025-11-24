"""Tests for file_handler module."""

import os
import tempfile
from pathlib import Path

import pytest

from mpress.file_handler import (
    FileValidationError,
    SUPPORTED_FORMATS,
    validate_file,
)


def test_validate_file_nonexistent():
    """Test validation of non-existent file."""
    with pytest.raises(FileValidationError, match="File not found"):
        validate_file("/nonexistent/file.png")


def test_validate_file_unsupported_format():
    """Test validation of unsupported file format."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        with pytest.raises(FileValidationError, match="Unsupported file format"):
            validate_file(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_validate_file_supported_formats():
    """Test that all supported formats are recognized."""
    assert ".png" in SUPPORTED_FORMATS
    assert ".jpg" in SUPPORTED_FORMATS
    assert ".jpeg" in SUPPORTED_FORMATS
    assert ".mov" in SUPPORTED_FORMATS
    assert ".mp4" in SUPPORTED_FORMATS
    assert ".webm" in SUPPORTED_FORMATS


def test_validate_file_image_format():
    """Test validation of image file."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"fake png data")
    try:
        path, file_type = validate_file(tmp_path)
        assert isinstance(path, Path)
        assert file_type == "image"
    finally:
        os.unlink(tmp_path)


def test_validate_file_video_format():
    """Test validation of video file."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"fake mp4 data")
    try:
        path, file_type = validate_file(tmp_path)
        assert isinstance(path, Path)
        assert file_type == "video"
    finally:
        os.unlink(tmp_path)

