from datetime import datetime, timezone
from ..extensions import db


class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False)  # basic, story, special, action, act
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    image = db.relationship('Media', backref='programs', lazy=True)

    CATEGORIES = {
        'basic': '일상',
        'story': '놀이 이야기',
        'special': '학부모 참여수업',
        'action': '특별 활동',
        'act': '체험',
    }

    def __repr__(self):
        return f'<Program {self.category}/{self.title}>'

    @property
    def category_label(self):
        return self.CATEGORIES.get(self.category, self.category)
