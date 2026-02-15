import calendar
from flask import Blueprint, render_template, send_from_directory, current_app, request, abort
from ..models import HeroSlide, Program, Gallery, SiteInfo, Notice, Teacher, Event, MealPlan, ParentNote, Popup, DailySchedule, DownloadFile
from ..extensions import db
from ..utils.korean_holidays import get_holidays_for_month
from datetime import date, timedelta, datetime

public_bp = Blueprint('public', __name__)


def _get_site_info():
    """Helper: load all site_info as a dict."""
    site_info = {}
    for key in SiteInfo.KEYS:
        site_info[key] = SiteInfo.get_value(key, SiteInfo.KEYS[key])
    return site_info


@public_bp.route('/')
def index():
    """Homepage with highlights."""
    hero_slides = HeroSlide.query.filter_by(is_active=True).order_by(HeroSlide.sort_order).all()
    site_info = _get_site_info()

    # Highlights
    notices = Notice.query.order_by(Notice.is_pinned.desc(), Notice.created_at.desc()).limit(3).all()
    upcoming_events = Event.query.filter(Event.event_date >= date.today()).order_by(Event.event_date).limit(3).all()
    gallery_items = Gallery.query.order_by(Gallery.sort_order).limit(4).all()

    # Active popups
    today = date.today()
    popups = Popup.query.filter_by(is_active=True).order_by(Popup.sort_order).all()
    active_popups = [p for p in popups if p.is_currently_active]

    return render_template('public/index.html',
        hero_slides=hero_slides,
        site_info=site_info,
        notices=notices,
        upcoming_events=upcoming_events,
        gallery_items=gallery_items,
        active_popups=active_popups,
    )


@public_bp.route('/about')
def about():
    """About page - principal greeting, features, operation info."""
    site_info = _get_site_info()
    principal = Teacher.query.filter_by(title='원장').first()
    daily_schedule = DailySchedule.query.order_by(DailySchedule.sort_order, DailySchedule.time_label).all()

    # Parse newline-separated SiteInfo values for lists
    admission_raw = SiteInfo.get_value('admission_details', '')
    admission_details = [line.strip() for line in admission_raw.split('\n') if line.strip()] if admission_raw else []

    meal_raw = SiteInfo.get_value('meal_features', '')
    meal_features = [line.strip() for line in meal_raw.split('\n') if line.strip()] if meal_raw else []

    download_files = DownloadFile.query.filter_by(is_active=True).order_by(DownloadFile.sort_order).all()

    return render_template('public/about.html',
        site_info=site_info,
        principal=principal,
        daily_schedule=daily_schedule,
        admission_details=admission_details,
        meal_features=meal_features,
        download_files=download_files,
        page_title='어린이집 소개',
        breadcrumb_items=[{'label': '어린이집 소개'}],
    )


@public_bp.route('/teachers')
def teachers():
    """Teacher profiles page."""
    teachers_list = Teacher.query.order_by(Teacher.sort_order).all()
    return render_template('public/teachers.html',
        teachers=teachers_list,
        page_title='교사소개',
        breadcrumb_items=[{'label': '교사소개'}],
    )


@public_bp.route('/programs')
def programs():
    """Programs page with category tabs."""
    programs_data = {}
    for category in ['basic', 'story', 'special', 'action', 'act']:
        programs_data[category] = Program.query.filter_by(category=category).order_by(Program.sort_order).all()
    return render_template('public/programs.html',
        programs=programs_data,
        page_title='교육과정',
        breadcrumb_items=[{'label': '교육과정'}],
    )


@public_bp.route('/gallery')
def gallery():
    """Activity gallery page."""
    gallery_items = Gallery.query.order_by(Gallery.sort_order).all()
    return render_template('public/gallery.html',
        gallery_items=gallery_items,
        page_title='활동 앨범',
        breadcrumb_items=[{'label': '교육과정', 'url': '/programs'}, {'label': '활동 앨범'}],
    )


@public_bp.route('/notices')
def notices():
    """Notice list with pagination."""
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.order_by(
        Notice.is_pinned.desc(), Notice.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    return render_template('public/notices/list.html',
        pagination=pagination,
        notices=pagination.items,
        page_title='공지사항',
        breadcrumb_items=[{'label': '알림마당'}, {'label': '공지사항'}],
    )


@public_bp.route('/notices/<int:notice_id>')
def notice_detail(notice_id):
    """Notice detail with prev/next navigation."""
    notice = Notice.query.get_or_404(notice_id)

    prev_notice = Notice.query.filter(
        Notice.created_at < notice.created_at
    ).order_by(Notice.created_at.desc()).first()

    next_notice = Notice.query.filter(
        Notice.created_at > notice.created_at
    ).order_by(Notice.created_at.asc()).first()

    return render_template('public/notices/detail.html',
        notice=notice,
        prev_notice=prev_notice,
        next_notice=next_notice,
        page_title='공지사항',
        breadcrumb_items=[
            {'label': '알림마당'},
            {'label': '공지사항', 'url': '/notices'},
            {'label': notice.title}
        ],
    )


@public_bp.route('/parent-notes')
def parent_notes():
    """Parent notes list with class filter."""
    page = request.args.get('page', 1, type=int)
    target_class = request.args.get('class', 'all')

    query = ParentNote.query
    if target_class != 'all':
        query = query.filter_by(target_class=target_class)

    pagination = query.order_by(
        ParentNote.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template('public/parent_notes/list.html',
        pagination=pagination,
        notes=pagination.items,
        target_class=target_class,
        target_classes=ParentNote.TARGET_CLASSES,
        page_title='가정통신문',
        breadcrumb_items=[{'label': '알림마당'}, {'label': '가정통신문'}],
    )


@public_bp.route('/parent-notes/<int:note_id>')
def parent_note_detail(note_id):
    """Parent note detail."""
    note = ParentNote.query.get_or_404(note_id)

    prev_note = ParentNote.query.filter(
        ParentNote.created_at < note.created_at
    ).order_by(ParentNote.created_at.desc()).first()

    next_note = ParentNote.query.filter(
        ParentNote.created_at > note.created_at
    ).order_by(ParentNote.created_at.asc()).first()

    return render_template('public/parent_notes/detail.html',
        note=note,
        prev_note=prev_note,
        next_note=next_note,
        page_title='가정통신문',
        breadcrumb_items=[
            {'label': '알림마당'},
            {'label': '가정통신문', 'url': '/parent-notes'},
            {'label': note.title}
        ],
    )


@public_bp.route('/meals')
def meals():
    """Weekly meal plan table view."""
    week_str = request.args.get('week')
    if week_str:
        try:
            week_start = datetime.strptime(week_str, '%Y-%m-%d').date()
        except ValueError:
            week_start = date.today()
    else:
        week_start = date.today()

    # Adjust to Monday of the week
    week_start = week_start - timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=4)  # Friday

    prev_week = week_start - timedelta(weeks=1)
    next_week = week_start + timedelta(weeks=1)

    # Query meals for the week
    meal_plans = MealPlan.query.filter(
        MealPlan.plan_date >= week_start,
        MealPlan.plan_date <= week_end
    ).order_by(MealPlan.plan_date, MealPlan.meal_type).all()

    # Organize into a dict: {date_str: {meal_type: meal}}
    meals_by_date = {}
    for meal in meal_plans:
        date_key = meal.plan_date.strftime('%Y-%m-%d')
        if date_key not in meals_by_date:
            meals_by_date[date_key] = {}
        meals_by_date[date_key][meal.meal_type] = meal

    # Generate weekdays list
    weekdays = []
    for i in range(5):
        d = week_start + timedelta(days=i)
        weekdays.append(d)

    return render_template('public/meals.html',
        weekdays=weekdays,
        meals_by_date=meals_by_date,
        week_start=week_start,
        week_end=week_end,
        prev_week=prev_week,
        next_week=next_week,
        meal_types=MealPlan.MEAL_TYPES,
        page_title='급식관리',
        breadcrumb_items=[{'label': '급식관리'}],
    )


@public_bp.route('/events')
def events():
    """Monthly event list."""
    month_str = request.args.get('month')
    if month_str:
        try:
            current_month = datetime.strptime(month_str + '-01', '%Y-%m-%d').date()
        except ValueError:
            current_month = date.today().replace(day=1)
    else:
        current_month = date.today().replace(day=1)

    # Calculate next month
    if current_month.month == 12:
        next_month_start = current_month.replace(year=current_month.year + 1, month=1)
    else:
        next_month_start = current_month.replace(month=current_month.month + 1)

    prev_month = current_month - timedelta(days=1)
    prev_month = prev_month.replace(day=1)

    events_list = Event.query.filter(
        Event.event_date >= current_month,
        Event.event_date < next_month_start
    ).order_by(Event.event_date).all()

    # Calendar grid data
    year = current_month.year
    month = current_month.month
    cal = calendar.Calendar(firstweekday=6)  # Sunday first
    month_days = cal.monthdayscalendar(year, month)

    # Events grouped by day
    events_by_day = {}
    for ev in events_list:
        day = ev.event_date.day
        events_by_day.setdefault(day, []).append(ev)

    # Korean holidays for this month
    holidays = get_holidays_for_month(year, month)

    today = date.today()

    return render_template('public/events.html',
        events=events_list,
        current_month=current_month,
        prev_month=prev_month,
        next_month=next_month_start,
        month_days=month_days,
        events_by_day=events_by_day,
        holidays=holidays,
        today=today,
        page_title='행사일정',
        breadcrumb_items=[{'label': '행사일정'}],
    )


@public_bp.route('/contact')
def contact():
    """Contact page with map."""
    site_info = _get_site_info()
    return render_template('public/contact.html',
        site_info=site_info,
        page_title='오시는 길',
        breadcrumb_items=[{'label': '오시는 길'}],
    )


@public_bp.route('/robots.txt')
def robots():
    return send_from_directory(current_app.static_folder, 'robots.txt')


@public_bp.route('/sitemap.xml')
def sitemap():
    return send_from_directory(current_app.static_folder, 'sitemap.xml')
