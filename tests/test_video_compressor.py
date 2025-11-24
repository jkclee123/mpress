"""Tests for video_compressor module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mpress.video_compressor import (
    FFmpegNotFoundError,
    VideoCompressionError,
    check_ffmpeg_available,
    compress_video,
)


def test_check_ffmpeg_available():
    """Test FFmpeg availability check."""
    # This will check the actual system
    result = check_ffmpeg_available()
    assert isinstance(result, bool)


@patch("mpress.video_compressor.shutil.which")
def test_compress_video_ffmpeg_not_found(mock_which):
    """Test compression when FFmpeg is not found."""
    mock_which.return_value = None
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.mp4"
        input_path.write_bytes(b"fake video data")
        with pytest.raises(FFmpegNotFoundError):
            compress_video(input_path)


def test_compress_video_unsupported_format():
    """Test compression of unsupported video format."""
    # Only test if FFmpeg is available
    if not check_ffmpeg_available():
        pytest.skip("FFmpeg not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.avi"
        input_path.write_bytes(b"fake video data")
        with pytest.raises(VideoCompressionError, match="Unsupported video format"):
            compress_video(input_path)

