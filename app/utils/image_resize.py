"""Image resize and compression utility."""
from PIL import Image
import os


def resize_and_compress(filepath, max_width=1600, max_height=1200, quality=82):
    """Resize image if larger than max dimensions and compress.

    Overwrites the original file with the optimized version.
    Skips GIF and SVG files. Converts PNG to JPEG if very large.

    Returns the (possibly updated) filepath and file size.
    """
    ext = filepath.rsplit('.', 1)[-1].lower()
    if ext in ('gif', 'svg'):
        return filepath, os.path.getsize(filepath)

    try:
        img = Image.open(filepath)
    except Exception:
        return filepath, os.path.getsize(filepath)

    # Handle EXIF rotation
    try:
        from PIL import ExifTags
        for orientation in ExifTags.TAGS:
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif and orientation in exif:
            rot = exif[orientation]
            if rot == 3:
                img = img.rotate(180, expand=True)
            elif rot == 6:
                img = img.rotate(270, expand=True)
            elif rot == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, TypeError):
        pass

    original_w, original_h = img.size
    needs_resize = original_w > max_width or original_h > max_height

    if needs_resize:
        img.thumbnail((max_width, max_height), Image.LANCZOS)

    # Convert RGBA to RGB for JPEG saving
    if img.mode in ('RGBA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[3])
        img = background

    # Save as JPEG for best compression (unless it's already webp)
    if ext == 'webp':
        img.save(filepath, 'WEBP', quality=quality, optimize=True)
    elif ext == 'png' and os.path.getsize(filepath) > 500_000:
        # Large PNG → convert to JPEG
        new_filepath = filepath.rsplit('.', 1)[0] + '.jpg'
        img.save(new_filepath, 'JPEG', quality=quality, optimize=True)
        os.remove(filepath)
        filepath = new_filepath
    else:
        # Save as JPEG
        if ext in ('jpg', 'jpeg'):
            img.save(filepath, 'JPEG', quality=quality, optimize=True)
        elif ext == 'png':
            img.save(filepath, 'PNG', optimize=True)

    file_size = os.path.getsize(filepath)
    return filepath, file_size
