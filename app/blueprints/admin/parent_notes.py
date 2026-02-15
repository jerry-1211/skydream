from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import ParentNote


@admin_bp.route('/parent-notes/')
def parent_notes_list():
    page = request.args.get('page', 1, type=int)
    pagination = ParentNote.query.order_by(ParentNote.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/parent_notes/list.html', pagination=pagination)


@admin_bp.route('/parent-notes/create', methods=['GET', 'POST'])
def parent_notes_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        target_class = request.form.get('target_class', 'all').strip()

        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.', 'error')
            return render_template('admin/parent_notes/form.html', note=None, target_classes=ParentNote.TARGET_CLASSES)

        note = ParentNote(
            title=title,
            content=content,
            target_class=target_class,
        )
        db.session.add(note)
        db.session.commit()
        flash('학부모 알림이 등록되었습니다.', 'success')
        return redirect(url_for('admin.parent_notes_list'))

    return render_template('admin/parent_notes/form.html', note=None, target_classes=ParentNote.TARGET_CLASSES)


@admin_bp.route('/parent-notes/<int:id>/edit', methods=['GET', 'POST'])
def parent_notes_edit(id):
    note = ParentNote.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        target_class = request.form.get('target_class', 'all').strip()

        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.', 'error')
            return render_template('admin/parent_notes/form.html', note=note, target_classes=ParentNote.TARGET_CLASSES)

        note.title = title
        note.content = content
        note.target_class = target_class
        db.session.commit()
        flash('학부모 알림이 수정되었습니다.', 'success')
        return redirect(url_for('admin.parent_notes_list'))

    return render_template('admin/parent_notes/form.html', note=note, target_classes=ParentNote.TARGET_CLASSES)


@admin_bp.route('/parent-notes/<int:id>/delete', methods=['POST'])
def parent_notes_delete(id):
    note = ParentNote.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('학부모 알림이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.parent_notes_list'))
