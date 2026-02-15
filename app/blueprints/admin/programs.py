from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Program


@admin_bp.route('/programs/')
def programs_list():
    current_cat = request.args.get('category', 'all')
    categories = Program.CATEGORIES

    query = Program.query
    if current_cat != 'all':
        query = query.filter_by(category=current_cat)

    programs = query.order_by(Program.sort_order).all()
    return render_template('admin/programs/list.html',
                           programs=programs,
                           categories=categories,
                           current_cat=current_cat)


@admin_bp.route('/programs/create', methods=['GET', 'POST'])
def programs_create():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not category or not title:
            flash('카테고리와 제목을 입력해주세요.', 'error')
            return render_template('admin/programs/form.html', program=None, categories=Program.CATEGORIES)

        image_id = handle_image_upload('photo', category='program', alt_text=title)

        program = Program(
            category=category,
            title=title,
            description=description,
            image_id=image_id,
            sort_order=sort_order,
        )
        db.session.add(program)
        db.session.commit()
        flash('프로그램이 등록되었습니다.', 'success')
        return redirect(url_for('admin.programs_list'))

    return render_template('admin/programs/form.html', program=None, categories=Program.CATEGORIES)


@admin_bp.route('/programs/<int:id>/edit', methods=['GET', 'POST'])
def programs_edit(id):
    program = Program.query.get_or_404(id)

    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not category or not title:
            flash('카테고리와 제목을 입력해주세요.', 'error')
            return render_template('admin/programs/form.html', program=program, categories=Program.CATEGORIES)

        new_image_id = handle_image_upload('photo', category='program', alt_text=title)
        if new_image_id:
            program.image_id = new_image_id

        program.category = category
        program.title = title
        program.description = description
        program.sort_order = sort_order
        db.session.commit()
        flash('프로그램이 수정되었습니다.', 'success')
        return redirect(url_for('admin.programs_list'))

    return render_template('admin/programs/form.html', program=program, categories=Program.CATEGORIES)


@admin_bp.route('/programs/<int:id>/delete', methods=['POST'])
def programs_delete(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    flash('프로그램이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.programs_list'))
