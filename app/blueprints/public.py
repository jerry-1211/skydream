from flask import Blueprint, render_template, send_from_directory, current_app
from ..models import HeroSlide, Program, Gallery, SiteInfo, Notice, Teacher, Event, MealPlan
from ..extensions import db

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    # Hero slides (active only, ordered)
    hero_slides = HeroSlide.query.filter_by(is_active=True).order_by(HeroSlide.sort_order).all()

    # Programs grouped by category
    programs = {}
    for category in ['basic', 'story', 'special', 'action', 'act']:
        programs[category] = Program.query.filter_by(category=category).order_by(Program.sort_order).all()

    # Gallery items
    gallery_items = Gallery.query.order_by(Gallery.sort_order).all()

    # Site info (as dict)
    site_info = {}
    for key in SiteInfo.KEYS:
        site_info[key] = SiteInfo.get_value(key, SiteInfo.KEYS[key])

    # Recent notices (top 5 pinned first)
    notices = Notice.query.order_by(Notice.is_pinned.desc(), Notice.created_at.desc()).limit(5).all()

    # Teachers
    teachers = Teacher.query.order_by(Teacher.sort_order).all()

    # Upcoming events
    from datetime import date
    upcoming_events = Event.query.filter(Event.event_date >= date.today()).order_by(Event.event_date).limit(5).all()

    return render_template('public/index.html',
        hero_slides=hero_slides,
        programs=programs,
        gallery_items=gallery_items,
        site_info=site_info,
        notices=notices,
        teachers=teachers,
        upcoming_events=upcoming_events,
    )


@public_bp.route('/robots.txt')
def robots():
    return send_from_directory(current_app.static_folder, 'robots.txt')


@public_bp.route('/sitemap.xml')
def sitemap():
    return send_from_directory(current_app.static_folder, 'sitemap.xml')
