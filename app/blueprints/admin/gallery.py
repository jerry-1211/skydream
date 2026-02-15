from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Gallery


@admin_bp.route('/gallery/')
def gallery_list():
    page = request.args.get('page', 1, type=int)
    pagination = Gallery.query.order_by(Gallery.sort_order, Gallery.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/gallery/list.html', pagination=pagination)


@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
def gallery_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/gallery/form.html', gallery_item=None)

        image_id = handle_image_upload('photo', category='gallery', alt_text=title)

        gallery_item = Gallery(
            title=title,
            image_id=image_id,
            sort_order=sort_order,
        )
        db.session.add(gallery_item)
        db.session.commit()
        flash('갤러리 항목이 등록되었습니다.', 'success')
        return redirect(url_for('admin.gallery_list'))

    return render_template('admin/gallery/form.html', gallery_item=None)


@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
def gallery_edit(id):
    gallery_item = Gallery.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/gallery/form.html', gallery_item=gallery_item)

        new_image_id = handle_image_upload('photo', category='gallery', alt_text=title)
        if new_image_id:
            gallery_item.image_id = new_image_id

        gallery_item.title = title
        gallery_item.sort_order = sort_order
        db.session.commit()
        flash('갤러리 항목이 수정되었습니다.', 'success')
        return redirect(url_for('admin.gallery_list'))

    return render_template('admin/gallery/form.html', gallery_item=gallery_item)


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
def gallery_delete(id):
    gallery_item = Gallery.query.get_or_404(id)
    db.session.delete(gallery_item)
    db.session.commit()
    flash('갤러리 항목이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.gallery_list'))
