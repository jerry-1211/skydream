from . import admin_bp
from flask import render_template
from ...extensions import db
from ...models import Notice, Media, Program, Gallery, HeroSlide, MealPlan, Event, Teacher


@admin_bp.route('/')
def dashboard():
    stats = {
        'notices': db.session.query(Notice).count(),
        'media': db.session.query(Media).count(),
        'programs': db.session.query(Program).count(),
        'galleries': db.session.query(Gallery).count(),
        'hero_slides': db.session.query(HeroSlide).count(),
        'meals': db.session.query(MealPlan).count(),
        'events': db.session.query(Event).count(),
        'teachers': db.session.query(Teacher).count(),
    }
    return render_template('admin/dashboard.html', stats=stats)
