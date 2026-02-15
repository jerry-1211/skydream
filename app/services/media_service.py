"""Media processing service for upload-time image optimization."""
import os
import uuid
from pathlib import Path
from PIL import Image
from flask import current_app
from ..extensions import db
from ..models import Media


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
WEBP_QUALITY = 85
THUMB_SIZE = (300, 300)


def get_upload_dirs():
    """Get upload directory paths."""
    base = Path(current_app.static_folder) / 'uploads'
    return {
        'originals': base / 'originals',
        'webp': base / 'webp',
        'thumbnails': base / 'thumbnails',
    }


def ensure_upload_dirs():
    """Create upload directories if they don't exist."""
    for d in get_upload_dirs().values():
        d.mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS


def get_file_type(filename):
    """Determine if file is image or video."""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return 'image'
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return 'video'
    return None


def save_uploaded_file(file_storage, alt_text='', category='general'):
    """
    Process and save an uploaded file.
    Returns a Media model instance (not yet committed).
    """
    ensure_upload_dirs()
    dirs = get_upload_dirs()

    original_filename = file_storage.filename
    ext = original_filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}"
    file_type = get_file_type(original_filename)

    if file_type == 'image':
        # Save original
        orig_path = dirs['originals'] / f"{unique_name}.{ext}"
        file_storage.save(str(orig_path))
        file_size = orig_path.stat().st_size

        # Process image
        img = Image.open(orig_path)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize if too large (max 1920px width)
        if img.width > 1920:
            ratio = 1920 / img.width
            img = img.resize((1920, int(img.height * ratio)), Image.LANCZOS)
            img.save(str(orig_path), quality=90)

        # Generate WebP
        webp_path = dirs['webp'] / f"{unique_name}.webp"
        img.save(str(webp_path), 'WebP', quality=WEBP_QUALITY)

        # Generate thumbnail
        thumb_path = dirs['thumbnails'] / f"{unique_name}_thumb.webp"
        # Center crop
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        cropped = img.crop((left, top, left + min_dim, top + min_dim))
        thumb = cropped.resize(THUMB_SIZE, Image.LANCZOS)
        thumb.save(str(thumb_path), 'WebP', quality=WEBP_QUALITY)

        media = Media(
            filename=f"{unique_name}.{ext}",
            original_filename=original_filename,
            file_type='image',
            file_size=file_size,
            thumbnail_path=f"uploads/thumbnails/{unique_name}_thumb.webp",
            webp_path=f"uploads/webp/{unique_name}.webp",
            alt_text=alt_text,
            category=category,
        )
    else:
        # Video: just save
        video_path = dirs['originals'] / f"{unique_name}.{ext}"
        file_storage.save(str(video_path))
        file_size = video_path.stat().st_size

        media = Media(
            filename=f"{unique_name}.{ext}",
            original_filename=original_filename,
            file_type='video',
            file_size=file_size,
            alt_text=alt_text,
            category=category,
        )

    return media


def delete_media_files(media):
    """Delete all files associated with a Media record."""
    dirs = get_upload_dirs()

    # Delete original
    orig = dirs['originals'] / media.filename
    if orig.exists():
        orig.unlink()

    # Delete WebP
    if media.webp_path:
        webp = Path(current_app.static_folder) / media.webp_path
        if webp.exists():
            webp.unlink()

    # Delete thumbnail
    if media.thumbnail_path:
        thumb = Path(current_app.static_folder) / media.thumbnail_path
        if thumb.exists():
            thumb.unlink()
