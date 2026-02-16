from datetime import datetime, timezone
from ..extensions import db


class ParentNote(db.Model):
    __tablename__ = 'parent_notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    target_class = db.Column(db.String(50), default='all')  # all, 0세반, 1세반, 2세반
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))

    TARGET_CLASSES = {
        'all': '전체',
        'age0': '0세 (별반)',
        'age1': '1세 (달반)',
        'age2': '2세 (해반)',
    }

    @property
    def target_class_label(self):
        return self.TARGET_CLASSES.get(self.target_class, self.target_class)

    def __repr__(self):
        return f'<ParentNote {self.title}>'
