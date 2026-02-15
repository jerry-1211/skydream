"""Shared image upload helper for admin forms."""
import os
import uuid

from flask import current_app, request
from ...extensions import db
from ...models import Media

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}


def handle_image_upload(field_name='photo', category='general', alt_text=''):
    """Process an uploaded image file and return a Media id, or None.

    Call this from any admin route POST handler.  If the user uploaded a file
    via the given *field_name*, we save it and create a Media record.

    Returns:
        int | None  – the new Media.id, or None when no file was uploaded.
    """
    file = request.files.get(field_name)
    if not file or file.filename == '':
        return None

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    original_filename = file.filename
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    originals_dir = os.path.join(upload_folder, 'originals')
    os.makedirs(originals_dir, exist_ok=True)

    filepath = os.path.join(originals_dir, unique_filename)
    file.save(filepath)

    file_size = os.path.getsize(filepath)

    media = Media(
        filename=unique_filename,
        original_filename=original_filename,
        file_type='image',
        file_size=file_size,
        alt_text=alt_text or original_filename,
        category=category,
    )
    db.session.add(media)
    db.session.flush()  # get media.id without committing
    return media.id
