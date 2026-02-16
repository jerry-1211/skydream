from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Comment


@admin_bp.route('/comments/')
def comments_list():
    page = request.args.get('page', 1, type=int)
    content_type = request.args.get('type', '')

    query = Comment.query
    if content_type:
        query = query.filter_by(content_type=content_type)
    pagination = query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=20)

    return render_template('admin/comments/list.html',
                           pagination=pagination,
                           current_type=content_type)


@admin_bp.route('/comments/<int:id>/delete', methods=['POST'])
def comments_delete(id):
    comment = Comment.query.get_or_404(id)
    next_url = request.form.get('next', '')
    db.session.delete(comment)
    db.session.commit()
    flash('댓글이 삭제되었습니다.', 'success')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('admin.comments_list'))
