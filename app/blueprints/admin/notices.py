from . import admin_bp
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from ...extensions import db
from ...models import Notice
import os
import uuid


@admin_bp.route('/notices/')
def notices_list():
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.order_by(
        Notice.is_pinned.desc(), Notice.created_at.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/notices/list.html', pagination=pagination)


@admin_bp.route('/notices/create', methods=['GET', 'POST'])
def notices_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        is_pinned = request.form.get('is_pinned') == 'on'

        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.', 'error')
            return render_template('admin/notices/form.html', notice=None)

        notice = Notice(title=title, content=content, is_pinned=is_pinned)
        db.session.add(notice)
        db.session.commit()
        flash('공지사항이 등록되었습니다.', 'success')
        return redirect(url_for('admin.notices_list'))

    return render_template('admin/notices/form.html', notice=None)


@admin_bp.route('/notices/<int:id>/edit', methods=['GET', 'POST'])
def notices_edit(id):
    notice = Notice.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        is_pinned = request.form.get('is_pinned') == 'on'

        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.', 'error')
            return render_template('admin/notices/form.html', notice=notice)

        notice.title = title
        notice.content = content
        notice.is_pinned = is_pinned
        db.session.commit()
        flash('공지사항이 수정되었습니다.', 'success')
        return redirect(url_for('admin.notices_list'))

    return render_template('admin/notices/form.html', notice=notice)


@admin_bp.route('/notices/<int:id>/delete', methods=['POST'])
def notices_delete(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    flash('공지사항이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.notices_list'))


@admin_bp.route('/notices/upload-image', methods=['POST'])
def notice_image_upload():
    """Handle image upload from Summernote editor in notices.

    Accepts any image format that PIL can open (PNG, JPG, GIF, WEBP, BMP, TIFF, HEIC, etc.)
    and converts to web-friendly JPEG/PNG.
    """
    from PIL import Image

    try:
        file = request.files.get('file')
        if not file or file.filename == '':
            return jsonify({'error': '파일이 없습니다.'}), 400

        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        notice_dir = os.path.join(upload_folder, 'notices')
        os.makedirs(notice_dir, exist_ok=True)

        # Save temp file first
        temp_filename = f"{uuid.uuid4().hex}_temp"
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'bin'
        temp_path = os.path.join(notice_dir, f"{temp_filename}.{ext}")
        file.save(temp_path)

        # Try to open with PIL (supports all common formats)
        try:
            img = Image.open(temp_path)
            img.load()  # Force load to catch corrupt files
        except Exception:
            os.remove(temp_path)
            return jsonify({'error': '이미지 파일을 열 수 없습니다. 유효한 이미지 파일인지 확인해주세요.'}), 400

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

        # Resize if needed
        max_w, max_h = 1200, 1200
        if img.size[0] > max_w or img.size[1] > max_h:
            img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Determine output format: keep PNG for transparency, JPEG for everything else
        final_id = uuid.uuid4().hex
        if img.mode == 'RGBA' or (img.mode == 'P' and 'transparency' in img.info):
            out_ext = 'png'
            out_path = os.path.join(notice_dir, f"{final_id}.png")
            img.save(out_path, 'PNG', optimize=True)
        else:
            out_ext = 'jpg'
            out_path = os.path.join(notice_dir, f"{final_id}.jpg")
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(out_path, 'JPEG', quality=80, optimize=True)

        # Clean up temp file
        if os.path.exists(temp_path) and temp_path != out_path:
            os.remove(temp_path)

        final_filename = os.path.basename(out_path)
        img_url = url_for('static', filename=f'uploads/notices/{final_filename}')
        return jsonify({'url': img_url})

    except Exception as e:
        current_app.logger.error(f'Notice image upload error: {e}')
        return jsonify({'error': '이미지 업로드 중 오류가 발생했습니다.'}), 500
