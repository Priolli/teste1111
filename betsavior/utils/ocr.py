from io import BytesIO

from PIL import Image
import pytesseract


def extract_text(image_bytes: bytes) -> str:
    """Extract text from an image represented as raw bytes."""
    with Image.open(BytesIO(image_bytes)) as img:
        return pytesseract.image_to_string(img)
