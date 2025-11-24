"""Tests for image_compressor module."""

import os
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from mpress.image_compressor import ImageCompressionError, compress_image


def create_test_png(path: Path, size: tuple[int, int] = (100, 100)) -> None:
    """Create a test PNG file."""
    img = Image.new("RGB", size, color="red")
    img.save(path, "PNG")


def create_test_jpeg(path: Path, size: tuple[int, int] = (100, 100)) -> None:
    """Create a test JPEG file."""
    img = Image.new("RGB", size, color="blue")
    img.save(path, "JPEG", quality=95)


def test_compress_png():
    """Test PNG compression."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.png"
        create_test_png(input_path)

        # Get original size
        original_size = input_path.stat().st_size

        # Compress
        compress_image(input_path)

        # Check file still exists and is smaller or same size
        assert input_path.exists()
        compressed_size = input_path.stat().st_size
        assert compressed_size <= original_size


def test_compress_jpeg():
    """Test JPEG compression."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.jpg"
        create_test_jpeg(input_path)

        # Get original size
        original_size = input_path.stat().st_size

        # Compress
        compress_image(input_path)

        # Check file still exists and is smaller or same size
        assert input_path.exists()
        compressed_size = input_path.stat().st_size
        assert compressed_size <= original_size


def test_compress_image_nonexistent():
    """Test compression of non-existent file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "nonexistent.png"
        with pytest.raises(ImageCompressionError):
            compress_image(input_path)


def test_compress_image_unsupported_format():
    """Test compression of unsupported format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.txt"
        input_path.write_text("not an image")
        with pytest.raises(ImageCompressionError, match="Unsupported image format"):
            compress_image(input_path)

