from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Teacher


@admin_bp.route('/teachers/')
def teachers_list():
    teachers = Teacher.query.order_by(Teacher.sort_order).all()
    return render_template('admin/teachers/list.html', teachers=teachers)


@admin_bp.route('/teachers/create', methods=['GET', 'POST'])
def teachers_create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        greeting = request.form.get('greeting', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not name:
            flash('이름을 입력해주세요.', 'error')
            return render_template('admin/teachers/form.html', teacher=None)

        avatar = request.form.get('avatar', '').strip()
        photo_id = handle_image_upload('photo', category='teacher', alt_text=name)

        teacher = Teacher(
            name=name,
            title=title,
            greeting=greeting,
            photo_id=photo_id,
            avatar=avatar,
            sort_order=sort_order,
        )
        db.session.add(teacher)
        db.session.commit()
        flash('교사 정보가 등록되었습니다.', 'success')
        return redirect(url_for('admin.teachers_list'))

    return render_template('admin/teachers/form.html', teacher=None)


@admin_bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
def teachers_edit(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        greeting = request.form.get('greeting', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not name:
            flash('이름을 입력해주세요.', 'error')
            return render_template('admin/teachers/form.html', teacher=teacher)

        new_photo_id = handle_image_upload('photo', category='teacher', alt_text=name)
        if new_photo_id:
            teacher.photo_id = new_photo_id

        avatar = request.form.get('avatar', '').strip()

        teacher.name = name
        teacher.title = title
        teacher.greeting = greeting
        teacher.avatar = avatar
        if avatar:
            teacher.photo_id = None
        teacher.sort_order = sort_order
        db.session.commit()
        flash('교사 정보가 수정되었습니다.', 'success')
        return redirect(url_for('admin.teachers_list'))

    return render_template('admin/teachers/form.html', teacher=teacher)


@admin_bp.route('/teachers/<int:id>/delete', methods=['POST'])
def teachers_delete(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('교사 정보가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.teachers_list'))
