from . import admin_bp
from flask import render_template, request, redirect, url_for, flash, current_app
from ...extensions import db
from ...models import DownloadFile
import os
import uuid


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'hwp', 'hwpx', 'zip'}


@admin_bp.route('/download-files/')
def download_files_list():
    files = DownloadFile.query.order_by(DownloadFile.sort_order, DownloadFile.created_at.desc()).all()
    return render_template('admin/download_files/list.html', files=files)


@admin_bp.route('/download-files/create', methods=['GET', 'POST'])
def download_files_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        file = request.files.get('file')
        if not file or file.filename == '':
            flash('파일을 선택해주세요.', 'error')
            return render_template('admin/download_files/form.html', item=None)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/download_files/form.html', item=None)

        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in ALLOWED_EXTENSIONS:
            flash(f'허용되지 않는 파일 형식입니다. ({", ".join(ALLOWED_EXTENSIONS)})', 'error')
            return render_template('admin/download_files/form.html', item=None)

        original_filename = file.filename
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        download_dir = os.path.join(upload_folder, 'downloads')
        os.makedirs(download_dir, exist_ok=True)

        filepath = os.path.join(download_dir, unique_filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)

        download_file = DownloadFile(
            title=title,
            description=description,
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            sort_order=sort_order,
        )
        db.session.add(download_file)
        db.session.commit()
        flash('파일이 등록되었습니다.', 'success')
        return redirect(url_for('admin.download_files_list'))

    return render_template('admin/download_files/form.html', item=None)


@admin_bp.route('/download-files/<int:id>/edit', methods=['GET', 'POST'])
def download_files_edit(id):
    item = DownloadFile.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/download_files/form.html', item=item)

        # Handle new file upload (optional on edit)
        file = request.files.get('file')
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
            if ext not in ALLOWED_EXTENSIONS:
                flash('허용되지 않는 파일 형식입니다.', 'error')
                return render_template('admin/download_files/form.html', item=item)

            # Delete old file
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            old_path = os.path.join(upload_folder, 'downloads', item.filename)
            if os.path.exists(old_path):
                os.remove(old_path)

            original_filename = file.filename
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            download_dir = os.path.join(upload_folder, 'downloads')
            filepath = os.path.join(download_dir, unique_filename)
            file.save(filepath)

            item.filename = unique_filename
            item.original_filename = original_filename
            item.file_size = os.path.getsize(filepath)

        item.title = title
        item.description = description
        item.sort_order = sort_order
        item.is_active = is_active
        db.session.commit()
        flash('파일 정보가 수정되었습니다.', 'success')
        return redirect(url_for('admin.download_files_list'))

    return render_template('admin/download_files/form.html', item=item)


@admin_bp.route('/download-files/<int:id>/delete', methods=['POST'])
def download_files_delete(id):
    item = DownloadFile.query.get_or_404(id)

    # Delete physical file
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    filepath = os.path.join(upload_folder, 'downloads', item.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(item)
    db.session.commit()
    flash('파일이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.download_files_list'))
