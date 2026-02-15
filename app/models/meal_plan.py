from datetime import datetime, date, timezone
from ..extensions import db
import json


class MealPlan(db.Model):
    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    plan_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, snack
    menu_items_json = db.Column(db.Text, default='[]')
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    image = db.relationship('Media', backref='meal_plans', lazy=True)

    MEAL_TYPES = {
        'breakfast': '아침',
        'lunch': '점심',
        'snack': '간식',
    }

    @property
    def menu_items(self):
        try:
            return json.loads(self.menu_items_json)
        except (json.JSONDecodeError, TypeError):
            return []

    @menu_items.setter
    def menu_items(self, items):
        self.menu_items_json = json.dumps(items, ensure_ascii=False)

    @property
    def meal_type_label(self):
        return self.MEAL_TYPES.get(self.meal_type, self.meal_type)

    def __repr__(self):
        return f'<MealPlan {self.plan_date} {self.meal_type}>'
