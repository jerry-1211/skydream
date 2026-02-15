from datetime import datetime, timezone
from ..extensions import db


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    file_size = db.Column(db.Integer)  # bytes
    thumbnail_path = db.Column(db.String(255))
    webp_path = db.Column(db.String(255))
    alt_text = db.Column(db.String(500), default='')
    category = db.Column(db.String(50), default='general')  # general, hero, program, gallery, teacher, meal, etc.
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Media {self.original_filename}>'

    @property
    def is_image(self):
        return self.file_type == 'image'

    @property
    def is_video(self):
        return self.file_type == 'video'
