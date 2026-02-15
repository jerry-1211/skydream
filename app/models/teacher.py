from datetime import datetime, timezone
from ..extensions import db


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), default='')  # e.g., '원장', '보육교사'
    greeting = db.Column(db.Text, default='')
    photo_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    photo = db.relationship('Media', backref='teachers', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'
