"""Video compression using FFmpeg."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from mpress.utils import atomic_replace


class VideoCompressionError(Exception):
    """Exception raised when video compression fails."""

    pass


class FFmpegNotFoundError(VideoCompressionError):
    """Exception raised when FFmpeg is not found on the system."""

    pass


def check_ffmpeg_available() -> bool:
    """
    Check if FFmpeg is available on the system.

    Returns:
        True if FFmpeg is available, False otherwise
    """
    return shutil.which("ffmpeg") is not None


def get_ffmpeg_path() -> str:
    """
    Get the path to the FFmpeg executable.

    Returns:
        Path to FFmpeg executable

    Raises:
        FFmpegNotFoundError: If FFmpeg is not found
    """
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise FFmpegNotFoundError(
            "FFmpeg is not installed or not in PATH. "
            "Please install FFmpeg: brew install ffmpeg"
        )
    return ffmpeg_path


def compress_mov_mp4(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Compress a MOV or MP4 video using H.264 codec with CRF 23.

    Args:
        input_path: Path to the input video file
        output_path: Path for the output file (if None, uses temp file)

    Returns:
        Path to the compressed file

    Raises:
        VideoCompressionError: If compression fails
    """
    if output_path is None:
        output_path = input_path.parent / f".{input_path.name}.tmp{input_path.suffix}"

    ffmpeg_path = get_ffmpeg_path()

    # Build FFmpeg command
    # -i: input file
    # -c:v libx264: use H.264 video codec
    # -crf 23: constant rate factor (quality setting, lower = better quality)
    # -preset medium: encoding speed vs compression tradeoff
    # -c:a copy: copy audio stream without re-encoding (faster, preserves quality)
    # -y: overwrite output file without asking
    cmd = [
        ffmpeg_path,
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-crf",
        "28",
        "-preset",
        "medium",
        "-c:a",
        "copy",
        "-y",
        str(output_path),
    ]

    try:
        # Run FFmpeg with suppressed output (errors go to stderr)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if result.returncode != 0:
            error_msg = result.stderr.decode("utf-8", errors="ignore")
            raise VideoCompressionError(
                f"FFmpeg compression failed for {input_path}: {error_msg}"
            )

        if not output_path.exists():
            raise VideoCompressionError(
                f"FFmpeg did not create output file: {output_path}"
            )

        return output_path

    except FileNotFoundError:
        raise FFmpegNotFoundError(
            "FFmpeg executable not found. Please install FFmpeg: brew install ffmpeg"
        )
    except subprocess.SubprocessError as e:
        raise VideoCompressionError(f"Failed to run FFmpeg for {input_path}: {e}") from e


def compress_webm(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Compress a WebM video using VP9 codec with CRF 30.

    Args:
        input_path: Path to the input video file
        output_path: Path for the output file (if None, uses temp file)

    Returns:
        Path to the compressed file

    Raises:
        VideoCompressionError: If compression fails
    """
    if output_path is None:
        output_path = input_path.parent / f".{input_path.name}.tmp{input_path.suffix}"

    ffmpeg_path = get_ffmpeg_path()

    # Build FFmpeg command
    # -i: input file
    # -c:v libvpx-vp9: use VP9 video codec
    # -crf 30: constant rate factor (quality setting)
    # -b:v 0: use CRF mode (variable bitrate)
    # -c:a libopus: use Opus audio codec (standard for WebM)
    # -y: overwrite output file without asking
    cmd = [
        ffmpeg_path,
        "-i",
        str(input_path),
        "-c:v",
        "libvpx-vp9",
        "-crf",
        "30",
        "-b:v",
        "0",
        "-c:a",
        "libopus",
        "-y",
        str(output_path),
    ]

    try:
        # Run FFmpeg with suppressed output (errors go to stderr)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if result.returncode != 0:
            error_msg = result.stderr.decode("utf-8", errors="ignore")
            raise VideoCompressionError(
                f"FFmpeg compression failed for {input_path}: {error_msg}"
            )

        if not output_path.exists():
            raise VideoCompressionError(
                f"FFmpeg did not create output file: {output_path}"
            )

        return output_path

    except FileNotFoundError:
        raise FFmpegNotFoundError(
            "FFmpeg executable not found. Please install FFmpeg: brew install ffmpeg"
        )
    except subprocess.SubprocessError as e:
        raise VideoCompressionError(f"Failed to run FFmpeg for {input_path}: {e}") from e


def compress_video(input_path: Path) -> None:
    """
    Compress a video file and replace the original atomically.

    Supports MOV, MP4, and WebM formats.

    Args:
        input_path: Path to the video file to compress

    Raises:
        VideoCompressionError: If compression fails or format is unsupported
        FFmpegNotFoundError: If FFmpeg is not available
    """
    extension = input_path.suffix.lower()

    # Check FFmpeg availability
    if not check_ffmpeg_available():
        raise FFmpegNotFoundError(
            "FFmpeg is not installed or not in PATH. "
            "Please install FFmpeg: brew install ffmpeg"
        )

    # Create temporary output file
    temp_output = input_path.parent / f".{input_path.name}.tmp{input_path.suffix}"

    try:
        if extension in (".mov", ".mp4"):
            compress_mov_mp4(input_path, temp_output)
        elif extension == ".webm":
            compress_webm(input_path, temp_output)
        else:
            raise VideoCompressionError(f"Unsupported video format: {extension}")

        # Atomically replace the original file
        atomic_replace(temp_output, input_path)

    except Exception as e:
        # Clean up temp file if it exists
        if temp_output.exists():
            try:
                temp_output.unlink()
            except OSError:
                pass

        # Re-raise the exception
        raise

