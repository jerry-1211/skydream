from datetime import datetime, timezone
from ..extensions import db


class HeroSlide(db.Model):
    __tablename__ = 'hero_slides'

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), default='')
    button_text = db.Column(db.String(50), default='')
    button_link = db.Column(db.String(200), default='')
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    image = db.relationship('Media', backref='hero_slides', lazy=True)

    def __repr__(self):
        return f'<HeroSlide {self.heading}>'
