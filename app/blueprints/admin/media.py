import os
import uuid
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash, current_app
from ...extensions import db
from ...models import Media


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return 'image'
    return 'video'


@admin_bp.route('/media/')
def media_list():
    page = request.args.get('page', 1, type=int)
    pagination = Media.query.order_by(Media.created_at.desc()).paginate(page=page, per_page=24)
    return render_template('admin/media/list.html', pagination=pagination)


@admin_bp.route('/media/upload', methods=['GET', 'POST'])
def media_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('파일을 선택해주세요.', 'error')
            return redirect(url_for('admin.media_upload'))

        file = request.files['file']
        if file.filename == '':
            flash('파일을 선택해주세요.', 'error')
            return redirect(url_for('admin.media_upload'))

        if not _allowed_file(file.filename):
            flash('지원하지 않는 파일 형식입니다.', 'error')
            return redirect(url_for('admin.media_upload'))

        original_filename = file.filename
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        originals_dir = os.path.join(upload_folder, 'originals')
        os.makedirs(originals_dir, exist_ok=True)

        filepath = os.path.join(originals_dir, unique_filename)
        file.save(filepath)

        file_size = os.path.getsize(filepath)
        file_type = _get_file_type(original_filename)
        alt_text = request.form.get('alt_text', '').strip()
        category = request.form.get('category', 'general').strip()

        media = Media(
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_type,
            file_size=file_size,
            alt_text=alt_text,
            category=category,
        )
        db.session.add(media)
        db.session.commit()
        flash('파일이 업로드되었습니다.', 'success')
        return redirect(url_for('admin.media_list'))

    return render_template('admin/media/upload.html')


@admin_bp.route('/media/<int:id>/delete', methods=['POST'])
def media_delete(id):
    media = Media.query.get_or_404(id)

    # Delete physical file
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    filepath = os.path.join(upload_folder, 'originals', media.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    # Delete thumbnail if exists
    if media.thumbnail_path:
        thumb_path = os.path.join(upload_folder, media.thumbnail_path)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    # Delete webp if exists
    if media.webp_path:
        webp_path = os.path.join(upload_folder, media.webp_path)
        if os.path.exists(webp_path):
            os.remove(webp_path)

    db.session.delete(media)
    db.session.commit()
    flash('파일이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.media_list'))
