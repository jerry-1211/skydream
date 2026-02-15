from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import HeroSlide


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
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not heading:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/hero_slides/form.html', slide=None)

        image_id = handle_image_upload('photo', category='hero', alt_text=heading)

        slide = HeroSlide(
            heading=heading,
            description=description,
            button_text=button_text,
            button_link=button_link,
            image_id=image_id,
            sort_order=sort_order,
            is_active=is_active,
        )
        db.session.add(slide)
        db.session.commit()
        flash('히어로 슬라이드가 등록되었습니다.', 'success')
        return redirect(url_for('admin.hero_slides_list'))

    return render_template('admin/hero_slides/form.html', slide=None)


@admin_bp.route('/hero-slides/<int:id>/edit', methods=['GET', 'POST'])
def hero_slides_edit(id):
    slide = HeroSlide.query.get_or_404(id)

    if request.method == 'POST':
        heading = request.form.get('heading', '').strip()
        description = request.form.get('description', '').strip()
        button_text = request.form.get('button_text', '').strip()
        button_link = request.form.get('button_link', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not heading:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/hero_slides/form.html', slide=slide)

        new_image_id = handle_image_upload('photo', category='hero', alt_text=heading)
        if new_image_id:
            slide.image_id = new_image_id

        slide.heading = heading
        slide.description = description
        slide.button_text = button_text
        slide.button_link = button_link
        slide.sort_order = sort_order
        slide.is_active = is_active
        db.session.commit()
        flash('히어로 슬라이드가 수정되었습니다.', 'success')
        return redirect(url_for('admin.hero_slides_list'))

    return render_template('admin/hero_slides/form.html', slide=slide)


@admin_bp.route('/hero-slides/<int:id>/delete', methods=['POST'])
def hero_slides_delete(id):
    slide = HeroSlide.query.get_or_404(id)
    db.session.delete(slide)
    db.session.commit()
    flash('히어로 슬라이드가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.hero_slides_list'))
