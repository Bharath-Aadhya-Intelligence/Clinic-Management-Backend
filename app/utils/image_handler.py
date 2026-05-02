from PIL import Image
import os
import uuid
from ..core.config import settings

def compress_image(image_file, filename: str) -> str:
    """
    Compresses an image to max 800x800px with 80% quality.
    Saves to the static directory and returns the relative file path.
    """
    # Create unique filename
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.jpg"  # Always save as jpg for consistent compression
    save_path = os.path.join(settings.STATIC_DIR, unique_filename)
    
    # Open image
    img = Image.open(image_file.file)
    
    # Convert to RGB if necessary (handles RGBA PNGs)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    # Resize maintaining aspect ratio
    img.thumbnail((800, 800), Image.LANCZOS)
    
    # Save with optimization and quality
    img.save(save_path, "JPEG", quality=80, optimize=True)
    
    return unique_filename

def delete_image(filename: str):
    """Deletes an image file from the static directory."""
    if not filename:
        return
    path = os.path.join(settings.STATIC_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
