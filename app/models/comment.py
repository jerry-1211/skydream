from datetime import datetime, timezone
from ..extensions import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20), nullable=False)  # 'notice' or 'parent_note'
    content_id = db.Column(db.Integer, nullable=False)
    author_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    body = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Comment {self.content_type}#{self.content_id} by {self.author_name}>'
