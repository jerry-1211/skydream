from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import DailySchedule


@admin_bp.route('/daily-schedule/')
def daily_schedule_list():
    items = DailySchedule.query.order_by(DailySchedule.sort_order, DailySchedule.time_label).all()
    return render_template('admin/daily_schedule/list.html', items=items)


@admin_bp.route('/daily-schedule/create', methods=['GET', 'POST'])
def daily_schedule_create():
    if request.method == 'POST':
        item = DailySchedule(
            time_label=request.form.get('time_label', '').strip(),
            icon_class=request.form.get('icon_class', 'fas fa-clock').strip(),
            title=request.form.get('title', '').strip(),
            description=request.form.get('description', '').strip(),
            sort_order=request.form.get('sort_order', 0, type=int),
        )
        if not item.time_label or not item.title:
            flash('시간과 제목을 입력해주세요.', 'error')
            return render_template('admin/daily_schedule/form.html', item=None)
        db.session.add(item)
        db.session.commit()
        flash('일과가 등록되었습니다.', 'success')
        return redirect(url_for('admin.daily_schedule_list'))
    return render_template('admin/daily_schedule/form.html', item=None)


@admin_bp.route('/daily-schedule/<int:id>/edit', methods=['GET', 'POST'])
def daily_schedule_edit(id):
    item = DailySchedule.query.get_or_404(id)
    if request.method == 'POST':
        item.time_label = request.form.get('time_label', '').strip()
        item.icon_class = request.form.get('icon_class', 'fas fa-clock').strip()
        item.title = request.form.get('title', '').strip()
        item.description = request.form.get('description', '').strip()
        item.sort_order = request.form.get('sort_order', 0, type=int)
        if not item.time_label or not item.title:
            flash('시간과 제목을 입력해주세요.', 'error')
            return render_template('admin/daily_schedule/form.html', item=item)
        db.session.commit()
        flash('일과가 수정되었습니다.', 'success')
        return redirect(url_for('admin.daily_schedule_list'))
    return render_template('admin/daily_schedule/form.html', item=item)


@admin_bp.route('/daily-schedule/<int:id>/delete', methods=['POST'])
def daily_schedule_delete(id):
    item = DailySchedule.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('일과가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.daily_schedule_list'))
