from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Event
from datetime import date
from calendar import monthrange, Calendar


@admin_bp.route('/events/')
def events_list():
    page = request.args.get('page', 1, type=int)
    month_str = request.args.get('month', '')

    try:
        if month_str:
            year, month = map(int, month_str.split('-'))
        else:
            today = date.today()
            year, month = today.year, today.month
    except (ValueError, AttributeError):
        today = date.today()
        year, month = today.year, today.month

    current_month = date(year, month, 1)
    _, last_day = monthrange(year, month)
    month_end = date(year, month, last_day)

    if month == 1:
        prev_month = date(year - 1, 12, 1)
    else:
        prev_month = date(year, month - 1, 1)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    query = Event.query.filter(
        Event.event_date >= current_month,
        Event.event_date <= month_end
    )
    pagination = query.order_by(Event.event_date.asc()).paginate(page=page, per_page=20)

    # Calendar grid data
    cal = Calendar(firstweekday=6)  # Sunday first
    month_days = cal.monthdayscalendar(year, month)
    events_by_day = {}
    all_events = Event.query.filter(
        Event.event_date >= current_month,
        Event.event_date <= month_end
    ).order_by(Event.event_date.asc()).all()
    for ev in all_events:
        day = ev.event_date.day
        events_by_day.setdefault(day, []).append(ev)

    today_obj = date.today()

    return render_template('admin/events/list.html',
                           pagination=pagination,
                           current_month=current_month,
                           prev_month=prev_month,
                           next_month=next_month,
                           month_days=month_days,
                           events_by_day=events_by_day,
                           today=today_obj,
                           year=year,
                           month=month)


@admin_bp.route('/events/create', methods=['GET', 'POST'])
def events_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        event_date_str = request.form.get('event_date', '').strip()
        event_type = request.form.get('event_type', 'general').strip()

        if not title or not event_date_str:
            flash('제목과 날짜를 입력해주세요.', 'error')
            return render_template('admin/events/form.html', event=None, event_types=Event.EVENT_TYPES)

        try:
            event_date = date.fromisoformat(event_date_str)
        except ValueError:
            flash('올바른 날짜 형식이 아닙니다.', 'error')
            return render_template('admin/events/form.html', event=None, event_types=Event.EVENT_TYPES)

        event = Event(
            title=title,
            description=description,
            event_date=event_date,
            event_type=event_type,
        )
        db.session.add(event)
        db.session.commit()
        flash('행사가 등록되었습니다.', 'success')
        return redirect(url_for('admin.events_list'))

    return render_template('admin/events/form.html', event=None, event_types=Event.EVENT_TYPES)


@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
def events_edit(id):
    event = Event.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        event_date_str = request.form.get('event_date', '').strip()
        event_type = request.form.get('event_type', 'general').strip()

        if not title or not event_date_str:
            flash('제목과 날짜를 입력해주세요.', 'error')
            return render_template('admin/events/form.html', event=event, event_types=Event.EVENT_TYPES)

        try:
            event_date = date.fromisoformat(event_date_str)
        except ValueError:
            flash('올바른 날짜 형식이 아닙니다.', 'error')
            return render_template('admin/events/form.html', event=event, event_types=Event.EVENT_TYPES)

        event.title = title
        event.description = description
        event.event_date = event_date
        event.event_type = event_type
        db.session.commit()
        flash('행사가 수정되었습니다.', 'success')
        return redirect(url_for('admin.events_list'))

    return render_template('admin/events/form.html', event=event, event_types=Event.EVENT_TYPES)


@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
def events_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('행사가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.events_list'))
