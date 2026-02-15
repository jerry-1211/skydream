from datetime import datetime, timezone
from ..extensions import db


class Gallery(db.Model):
    __tablename__ = 'galleries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    image = db.relationship('Media', backref='galleries', lazy=True)

    def __repr__(self):
        return f'<Gallery {self.title}>'
