from datetime import datetime, timezone
from ..extensions import db


class Popup(db.Model):
    __tablename__ = 'popups'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default='')  # HTML content
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    link_url = db.Column(db.String(500), default='')  # Click destination
    link_target = db.Column(db.String(20), default='_self')  # _self or _blank
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date, nullable=True)  # Show from this date (null = always)
    end_date = db.Column(db.Date, nullable=True)  # Show until this date (null = always)
    show_today_hide = db.Column(db.Boolean, default=True)  # Show "오늘 하루 보지 않기" checkbox
    position = db.Column(db.String(20), default='center')  # center, left, right
    width = db.Column(db.Integer, default=480)  # popup width in px
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    image = db.relationship('Media', backref='popups', lazy='joined')

    def __repr__(self):
        return f'<Popup {self.title}>'

    @property
    def is_currently_active(self):
        """Check if popup should be displayed right now."""
        if not self.is_active:
            return False
        today = datetime.now(timezone.utc).date()
        if self.start_date and today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False
        return True
