from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageOps


def load_image_from_buffer(file_buffer) -> Image.Image:
    """Load and standardize uploaded/captured image for inference."""
    raw = file_buffer.read()
    image = Image.open(BytesIO(raw))
    image = ImageOps.exif_transpose(image).convert("RGB")

    # Keep input size bounded for fast preview and inference.
    max_side = 1024
    if max(image.width, image.height) > max_side:
        image.thumbnail((max_side, max_side))

    return image
