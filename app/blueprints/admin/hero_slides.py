from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import HeroSlide, Media


@admin_bp.route('/hero-slides/')
def hero_slides_list():
    slides = HeroSlide.query.order_by(HeroSlide.sort_order).all()
    return render_template('admin/hero_slides/list.html', slides=slides)


@admin_bp.route('/hero-slides/create', methods=['GET', 'POST'])
def hero_slides_create():
    if request.method == 'POST':
        heading = request.form.get('heading', '').strip()
        description = request.form.get('description', '').strip()
        button_text = request.form.get('button_text', '').strip()
        button_link = request.form.get('button_link', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not heading:
            flash('제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/hero_slides/form.html', slide=None, media_list=media_list)

        slide = HeroSlide(
            heading=heading,
            description=description,
            button_text=button_text,
            button_link=button_link,
            image_id=image_id if image_id else None,
            sort_order=sort_order,
            is_active=is_active,
        )
        db.session.add(slide)
        db.session.commit()
        flash('히어로 슬라이드가 등록되었습니다.', 'success')
        return redirect(url_for('admin.hero_slides_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/hero_slides/form.html', slide=None, media_list=media_list)


@admin_bp.route('/hero-slides/<int:id>/edit', methods=['GET', 'POST'])
def hero_slides_edit(id):
    slide = HeroSlide.query.get_or_404(id)

    if request.method == 'POST':
        heading = request.form.get('heading', '').strip()
        description = request.form.get('description', '').strip()
        button_text = request.form.get('button_text', '').strip()
        button_link = request.form.get('button_link', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not heading:
            flash('제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/hero_slides/form.html', slide=slide, media_list=media_list)

        slide.heading = heading
        slide.description = description
        slide.button_text = button_text
        slide.button_link = button_link
        slide.image_id = image_id if image_id else None
        slide.sort_order = sort_order
        slide.is_active = is_active
        db.session.commit()
        flash('히어로 슬라이드가 수정되었습니다.', 'success')
        return redirect(url_for('admin.hero_slides_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/hero_slides/form.html', slide=slide, media_list=media_list)


@admin_bp.route('/hero-slides/<int:id>/delete', methods=['POST'])
def hero_slides_delete(id):
    slide = HeroSlide.query.get_or_404(id)
    db.session.delete(slide)
    db.session.commit()
    flash('히어로 슬라이드가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.hero_slides_list'))
