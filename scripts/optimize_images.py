#!/usr/bin/env python3
"""Batch optimize all existing images."""
import os
import sys
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / 'images'
UPLOADS_DIR = PROJECT_ROOT / 'app' / 'static' / 'uploads'

ORIGINALS_DIR = UPLOADS_DIR / 'originals'
WEBP_DIR = UPLOADS_DIR / 'webp'
THUMBNAILS_DIR = UPLOADS_DIR / 'thumbnails'

HERO_MAX_WIDTH = 1920
CARD_MAX_WIDTH = 800
THUMB_SIZE = (300, 300)
WEBP_QUALITY = 85

def ensure_dirs():
    for d in [ORIGINALS_DIR, WEBP_DIR, THUMBNAILS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def get_max_width(filepath):
    """Determine max width based on image type."""
    name = filepath.name.lower()
    if name.startswith('main'):
        return HERO_MAX_WIDTH
    return CARD_MAX_WIDTH

def resize_image(img, max_width):
    """Resize keeping aspect ratio."""
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        return img.resize((max_width, new_height), Image.LANCZOS)
    return img

def center_crop_thumbnail(img, size):
    """Center-crop to square then resize."""
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    cropped = img.crop((left, top, left + min_dim, top + min_dim))
    return cropped.resize(size, Image.LANCZOS)

def process_image(filepath):
    """Process a single image file."""
    try:
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        original_size = filepath.stat().st_size

        # Determine output path preserving subdirectory structure
        rel_path = filepath.relative_to(IMAGES_DIR)
        stem = rel_path.stem
        subdir = rel_path.parent

        # Ensure subdirectories exist
        (ORIGINALS_DIR / subdir).mkdir(parents=True, exist_ok=True)
        (WEBP_DIR / subdir).mkdir(parents=True, exist_ok=True)
        (THUMBNAILS_DIR / subdir).mkdir(parents=True, exist_ok=True)

        # 1. Resize original
        max_w = get_max_width(filepath)
        resized = resize_image(img, max_w)
        orig_out = ORIGINALS_DIR / subdir / f"{stem}.jpg"
        resized.save(orig_out, 'JPEG', quality=90)

        # 2. WebP conversion
        webp_out = WEBP_DIR / subdir / f"{stem}.webp"
        resized.save(webp_out, 'WebP', quality=WEBP_QUALITY)

        # 3. Thumbnail
        thumb = center_crop_thumbnail(img, THUMB_SIZE)
        thumb_out = THUMBNAILS_DIR / subdir / f"{stem}_thumb.webp"
        thumb.save(thumb_out, 'WebP', quality=WEBP_QUALITY)

        webp_size = webp_out.stat().st_size
        return original_size, webp_size

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return 0, 0

def main():
    ensure_dirs()

    total_original = 0
    total_optimized = 0
    count = 0

    extensions = {'.png', '.jpg', '.jpeg'}

    for filepath in sorted(IMAGES_DIR.rglob('*')):
        if filepath.suffix.lower() in extensions and filepath.is_file():
            orig_size, opt_size = process_image(filepath)
            if orig_size > 0:
                count += 1
                total_original += orig_size
                total_optimized += opt_size
                print(f"  {filepath.relative_to(IMAGES_DIR)}: {orig_size/1024:.0f}KB → {opt_size/1024:.0f}KB")

    print(f"\n{'='*50}")
    print(f"Processed: {count} images")
    print(f"Original total: {total_original/1024/1024:.1f} MB")
    print(f"Optimized total: {total_optimized/1024/1024:.1f} MB")
    if total_original > 0:
        reduction = (1 - total_optimized/total_original) * 100
        print(f"Reduction: {reduction:.1f}%")

if __name__ == '__main__':
    main()
