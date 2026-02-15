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
    """Handle image upload from Summernote editor in notices."""
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': '파일이 없습니다.'}), 400

    ext = file.filename.rsplit('.', 1)[-1].lower()
    allowed = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if ext not in allowed:
        return jsonify({'error': '허용되지 않는 파일 형식입니다.'}), 400

    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    notice_dir = os.path.join(upload_folder, 'notices')
    os.makedirs(notice_dir, exist_ok=True)

    filepath = os.path.join(notice_dir, unique_filename)
    file.save(filepath)

    img_url = url_for('static', filename=f'uploads/notices/{unique_filename}')
    return jsonify({'url': img_url})
