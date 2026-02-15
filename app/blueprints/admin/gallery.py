from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Gallery, Media


@admin_bp.route('/gallery/')
def gallery_list():
    page = request.args.get('page', 1, type=int)
    pagination = Gallery.query.order_by(Gallery.sort_order, Gallery.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/gallery/list.html', pagination=pagination)


@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
def gallery_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/gallery/form.html', gallery_item=None, media_list=media_list)

        gallery_item = Gallery(
            title=title,
            image_id=image_id if image_id else None,
            sort_order=sort_order,
        )
        db.session.add(gallery_item)
        db.session.commit()
        flash('갤러리 항목이 등록되었습니다.', 'success')
        return redirect(url_for('admin.gallery_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/gallery/form.html', gallery_item=None, media_list=media_list)


@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
def gallery_edit(id):
    gallery_item = Gallery.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/gallery/form.html', gallery_item=gallery_item, media_list=media_list)

        gallery_item.title = title
        gallery_item.image_id = image_id if image_id else None
        gallery_item.sort_order = sort_order
        db.session.commit()
        flash('갤러리 항목이 수정되었습니다.', 'success')
        return redirect(url_for('admin.gallery_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/gallery/form.html', gallery_item=gallery_item, media_list=media_list)


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
def gallery_delete(id):
    gallery_item = Gallery.query.get_or_404(id)
    db.session.delete(gallery_item)
    db.session.commit()
    flash('갤러리 항목이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.gallery_list'))
