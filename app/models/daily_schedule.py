from datetime import datetime, timezone
from ..extensions import db


class DailySchedule(db.Model):
    __tablename__ = 'daily_schedules'

    id = db.Column(db.Integer, primary_key=True)
    time_label = db.Column(db.String(10), nullable=False)  # e.g., "07:30"
    icon_class = db.Column(db.String(50), default='fas fa-clock')  # Font Awesome class
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), default='')
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<DailySchedule {self.time_label} {self.title}>'
