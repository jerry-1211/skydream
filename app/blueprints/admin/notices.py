from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Notice


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
