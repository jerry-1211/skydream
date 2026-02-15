from . import admin_bp
from flask import render_template
from ...extensions import db
from ...models import Notice, Event
from datetime import date


@admin_bp.route('/')
def dashboard():
    # Recent notices (latest 5)
    recent_notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()

    # Upcoming events (next 5)
    today = date.today()
    upcoming_events = Event.query.filter(
        Event.event_date >= today
    ).order_by(Event.event_date.asc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           recent_notices=recent_notices,
                           upcoming_events=upcoming_events)
