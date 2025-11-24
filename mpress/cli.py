"""Command-line interface for mpress."""

import argparse
import sys
from pathlib import Path

from mpress.file_handler import FileValidationError, validate_file
from mpress.image_compressor import ImageCompressionError, compress_image
from mpress.video_compressor import (
    FFmpegNotFoundError,
    VideoCompressionError,
    compress_video,
)


def process_file(file_path: str) -> tuple[bool, str]:
    """
    Process a single file: validate, compress, and replace.

    Args:
        file_path: Path to the file to process

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Validate file
        path, file_type = validate_file(file_path)

        # Compress based on file type
        if file_type == "image":
            compress_image(path)
            return True, f"Compressed: {file_path}"
        elif file_type == "video":
            compress_video(path)
            return True, f"Compressed: {file_path}"
        else:
            return False, f"Unknown file type: {file_path}"

    except FileValidationError as e:
        return False, f"Error: {e}"
    except ImageCompressionError as e:
        return False, f"Compression error: {e}"
    except VideoCompressionError as e:
        return False, f"Compression error: {e}"
    except FFmpegNotFoundError as e:
        return False, f"Error: {e}"
    except Exception as e:
        return False, f"Unexpected error processing {file_path}: {e}"


def main():
    """Main entry point for the mpress command."""
    parser = argparse.ArgumentParser(
        prog="mpress",
        description="Compress media files (PNG, JPG, JPEG, MOV, MP4, WebM)",
        epilog="Example: mpress image.png video.mp4",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Media files to compress",
    )

    args = parser.parse_args()

    # Handle no arguments case
    if not args.files:
        parser.print_usage()
        print("\nError: No files specified.")
        print("Usage: mpress <file1> [file2] [file3] ...")
        sys.exit(1)

    # Process files sequentially
    success_count = 0
    error_count = 0
    errors = []

    for file_path in args.files:
        success, message = process_file(file_path)
        if success:
            success_count += 1
            print(message)
        else:
            error_count += 1
            errors.append(message)
            print(message, file=sys.stderr)

    # Exit with appropriate code
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

