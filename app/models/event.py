from datetime import datetime, timezone
from ..extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    event_date = db.Column(db.Date, nullable=False)
    event_type = db.Column(db.String(50), default='general')  # general, field_trip, parent, holiday, special
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    EVENT_TYPES = {
        'general': '일반',
        'field_trip': '현장학습',
        'parent': '학부모 참여',
        'holiday': '휴원/공휴일',
        'special': '특별행사',
    }

    @property
    def event_type_label(self):
        return self.EVENT_TYPES.get(self.event_type, self.event_type)

    def __repr__(self):
        return f'<Event {self.title} on {self.event_date}>'
