"""Image compression using Pillow."""

from pathlib import Path
from typing import Optional

from PIL import Image

from mpress.utils import atomic_replace


class ImageCompressionError(Exception):
    """Exception raised when image compression fails."""

    pass


def compress_png(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Compress a PNG image.

    Args:
        input_path: Path to the input PNG file
        output_path: Path for the output file (if None, uses temp file)

    Returns:
        Path to the compressed file

    Raises:
        ImageCompressionError: If compression fails
    """
    if output_path is None:
        output_path = input_path.parent / f".{input_path.name}.tmp"

    try:
        # Open and compress the image
        with Image.open(input_path) as img:
            # Quantize to reduce file size (max 256 colors)
            # This effectively converts to P mode (palette-based)
            # For RGBA images, only FASTOCTREE (method 2) or LIBIMAGEQUANT (method 3) are valid
            if img.mode != "P":
                if img.mode == "RGBA":
                    # Use FASTOCTREE for RGBA images (method 2)
                    img = img.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
                else:
                    # Use MAXCOVERAGE for other modes (method 1) - better quality
                    img = img.quantize(colors=256, method=Image.Quantize.MAXCOVERAGE)

            img.save(
                output_path,
                "PNG",
                optimize=True,
                compress_level=9,
            )

        return output_path

    except Exception as e:
        raise ImageCompressionError(f"Failed to compress PNG {input_path}: {e}") from e


def compress_jpeg(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Compress a JPEG/JPG image.

    Args:
        input_path: Path to the input JPEG/JPG file
        output_path: Path for the output file (if None, uses temp file)

    Returns:
        Path to the compressed file

    Raises:
        ImageCompressionError: If compression fails
    """
    if output_path is None:
        output_path = input_path.parent / f".{input_path.name}.tmp"

    try:
        # Open and compress the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (JPEG doesn't support transparency)
            if img.mode in ("RGBA", "LA", "P"):
                # Create a white background for transparent images
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                else:
                    rgb_img.paste(img)
                img = rgb_img
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Save with compression
            img.save(
                output_path,
                "JPEG",
                quality=85,
                optimize=True,
            )

        return output_path

    except Exception as e:
        raise ImageCompressionError(f"Failed to compress JPEG {input_path}: {e}") from e


def compress_image(input_path: Path) -> None:
    """
    Compress an image file and replace the original atomically.

    Supports PNG, JPG, and JPEG formats.

    Args:
        input_path: Path to the image file to compress

    Raises:
        ImageCompressionError: If compression fails or format is unsupported
    """
    extension = input_path.suffix.lower()

    # Create temporary output file
    temp_output = input_path.parent / f".{input_path.name}.tmp"

    try:
        if extension == ".png":
            compress_png(input_path, temp_output)
        elif extension in (".jpg", ".jpeg"):
            compress_jpeg(input_path, temp_output)
        else:
            raise ImageCompressionError(f"Unsupported image format: {extension}")

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

