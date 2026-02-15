from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Program, Media


@admin_bp.route('/programs/')
def programs_list():
    programs = Program.query.order_by(Program.category, Program.sort_order).all()
    categories = Program.CATEGORIES
    return render_template('admin/programs/list.html', programs=programs, categories=categories)


@admin_bp.route('/programs/create', methods=['GET', 'POST'])
def programs_create():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not category or not title:
            flash('카테고리와 제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/programs/form.html', program=None, categories=Program.CATEGORIES, media_list=media_list)

        program = Program(
            category=category,
            title=title,
            description=description,
            image_id=image_id if image_id else None,
            sort_order=sort_order,
        )
        db.session.add(program)
        db.session.commit()
        flash('프로그램이 등록되었습니다.', 'success')
        return redirect(url_for('admin.programs_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/programs/form.html', program=None, categories=Program.CATEGORIES, media_list=media_list)


@admin_bp.route('/programs/<int:id>/edit', methods=['GET', 'POST'])
def programs_edit(id):
    program = Program.query.get_or_404(id)

    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_id = request.form.get('image_id', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not category or not title:
            flash('카테고리와 제목을 입력해주세요.', 'error')
            media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
            return render_template('admin/programs/form.html', program=program, categories=Program.CATEGORIES, media_list=media_list)

        program.category = category
        program.title = title
        program.description = description
        program.image_id = image_id if image_id else None
        program.sort_order = sort_order
        db.session.commit()
        flash('프로그램이 수정되었습니다.', 'success')
        return redirect(url_for('admin.programs_list'))

    media_list = Media.query.filter_by(file_type='image').order_by(Media.created_at.desc()).all()
    return render_template('admin/programs/form.html', program=program, categories=Program.CATEGORIES, media_list=media_list)


@admin_bp.route('/programs/<int:id>/delete', methods=['POST'])
def programs_delete(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    flash('프로그램이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.programs_list'))
