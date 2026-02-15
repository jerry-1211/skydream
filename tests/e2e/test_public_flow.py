"""Test public user navigation flow."""
from datetime import date, timedelta, datetime, timezone

from app.models import Notice, Event, MealPlan, ParentNote, Teacher, Media, Popup
from app.extensions import db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_notice(title='테스트 공지', content='테스트 내용', is_pinned=False):
    notice = Notice(title=title, content=content, is_pinned=is_pinned)
    db.session.add(notice)
    db.session.flush()
    return notice


def _seed_event(title='테스트 행사', description='설명', event_date=None, event_type='general'):
    if event_date is None:
        event_date = date.today() + timedelta(days=7)
    event = Event(title=title, description=description, event_date=event_date, event_type=event_type)
    db.session.add(event)
    db.session.flush()
    return event


def _seed_meal(plan_date=None, meal_type='lunch', menu_items=None):
    if plan_date is None:
        plan_date = date.today()
    if menu_items is None:
        menu_items = ['밥', '국', '반찬']
    meal = MealPlan(plan_date=plan_date, meal_type=meal_type)
    meal.menu_items = menu_items
    db.session.add(meal)
    db.session.flush()
    return meal


def _seed_parent_note(title='테스트 통신문', content='내용', target_class='all'):
    note = ParentNote(title=title, content=content, target_class=target_class)
    db.session.add(note)
    db.session.flush()
    return note


def _seed_teacher(name='테스트 교사', title='교사', greeting='안녕하세요'):
    media = Media(filename='teacher.jpeg', original_filename='teacher.jpeg',
                  file_type='image', file_size=0, alt_text=name, category='teacher')
    db.session.add(media)
    db.session.flush()
    teacher = Teacher(name=name, title=title, greeting=greeting,
                      photo_id=media.id, sort_order=1)
    db.session.add(teacher)
    db.session.flush()
    return teacher


def _seed_popup(title='테스트 팝업', content='팝업 내용', is_active=True):
    popup = Popup(title=title, content=content, is_active=is_active,
                  show_today_hide=True, position='center', width=480, sort_order=0)
    db.session.add(popup)
    db.session.flush()
    return popup


# ---------------------------------------------------------------------------
# Homepage Tests
# ---------------------------------------------------------------------------

def test_homepage_loads(client):
    """Homepage should return 200."""
    resp = client.get('/')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '하늘 꿈나무 어린이집' in html
    assert 'hero' in html


def test_homepage_has_navigation(client):
    """Homepage should have new navigation links."""
    resp = client.get('/')
    html = resp.data.decode()
    nav_items = ['어린이집 소개', '교사소개', '교육과정', '알림마당', '행사일정', '오시는 길']
    for item in nav_items:
        assert item in html, f'Missing nav item: {item}'


def test_homepage_has_highlights(client):
    """Homepage should have highlights section."""
    resp = client.get('/')
    html = resp.data.decode()
    assert '알림마당' in html
    assert '공지사항' in html
    assert '행사일정' in html
    assert '활동 앨범' in html


def test_homepage_menu_boxes(client):
    """Homepage menu boxes should link to actual pages."""
    resp = client.get('/')
    html = resp.data.decode()
    assert '/about' in html
    assert '/notices' in html
    assert '/contact' in html


# ---------------------------------------------------------------------------
# Subpage Tests - Status Codes
# ---------------------------------------------------------------------------

def test_about_page(client):
    """About page should return 200."""
    resp = client.get('/about')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '어린이집 소개' in html
    assert '원장 인사말' in html


def test_teachers_page(client):
    """Teachers page should return 200."""
    resp = client.get('/teachers')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '교사소개' in html


def test_programs_page(client):
    """Programs page should return 200."""
    resp = client.get('/programs')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '교육과정' in html


def test_gallery_page(client):
    """Gallery page should return 200."""
    resp = client.get('/gallery')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '활동 앨범' in html


def test_notices_page(client):
    """Notices list page should return 200."""
    resp = client.get('/notices')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '공지사항' in html


def test_parent_notes_page(client):
    """Parent notes list page should return 200."""
    resp = client.get('/parent-notes')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '가정통신문' in html


def test_meals_page(client):
    """Meals page should return 200."""
    resp = client.get('/meals')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '급식관리' in html


def test_events_page(client):
    """Events page should return 200."""
    resp = client.get('/events')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '행사일정' in html


def test_contact_page(client):
    """Contact page should return 200."""
    resp = client.get('/contact')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '오시는 길' in html
    assert 'maps.google.com' in html


# ---------------------------------------------------------------------------
# DB Data Integration Tests
# ---------------------------------------------------------------------------

def test_notice_detail_page(client, db):
    """Notice detail page should show notice content."""
    notice = _seed_notice(title='공지 테스트 제목', content='공지 테스트 내용입니다.')
    db.session.commit()

    resp = client.get(f'/notices/{notice.id}')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '공지 테스트 제목' in html
    assert '공지 테스트 내용입니다' in html


def test_notices_list_shows_db_data(client, db):
    """Notices list should show notices from DB."""
    _seed_notice(title='DB 공지사항 테스트')
    db.session.commit()

    resp = client.get('/notices')
    html = resp.data.decode()
    assert 'DB 공지사항 테스트' in html


def test_notices_pinned_first(client, db):
    """Pinned notices should appear first."""
    _seed_notice(title='일반 공지', is_pinned=False)
    _seed_notice(title='고정 공지', is_pinned=True)
    db.session.commit()

    resp = client.get('/notices')
    html = resp.data.decode()
    pinned_pos = html.find('고정 공지')
    normal_pos = html.find('일반 공지')
    assert pinned_pos < normal_pos, 'Pinned notice should appear before normal notice'


def test_parent_note_detail(client, db):
    """Parent note detail page should work."""
    note = _seed_parent_note(title='통신문 테스트', content='통신문 내용')
    db.session.commit()

    resp = client.get(f'/parent-notes/{note.id}')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '통신문 테스트' in html


def test_parent_notes_class_filter(client, db):
    """Parent notes should filter by class."""
    _seed_parent_note(title='전체 통신문', target_class='all')
    _seed_parent_note(title='0세반 통신문', target_class='age0')
    db.session.commit()

    resp = client.get('/parent-notes?class=age0')
    html = resp.data.decode()
    assert '0세반 통신문' in html


def test_teachers_with_data(client, db):
    """Teachers page should show teacher profiles."""
    _seed_teacher(name='김교사', title='담임교사', greeting='반갑습니다')
    db.session.commit()

    resp = client.get('/teachers')
    html = resp.data.decode()
    assert '김교사' in html
    assert '담임교사' in html


def test_meals_with_data(client, db):
    """Meals page should show meal plans."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    _seed_meal(plan_date=monday, meal_type='lunch', menu_items=['밥', '된장국', '김치'])
    db.session.commit()

    resp = client.get(f'/meals?week={monday.strftime("%Y-%m-%d")}')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '밥' in html


def test_events_with_data(client, db):
    """Events page should show event list."""
    event_date = date.today().replace(day=15)
    _seed_event(title='테스트 행사', event_date=event_date)
    db.session.commit()

    resp = client.get(f'/events?month={event_date.strftime("%Y-%m")}')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '테스트 행사' in html


def test_meals_week_navigation(client):
    """Meals page should have week navigation."""
    resp = client.get('/meals')
    html = resp.data.decode()
    assert '이전 주' in html
    assert '다음 주' in html


def test_events_month_navigation(client):
    """Events page should have month navigation."""
    resp = client.get('/events')
    html = resp.data.decode()
    assert '이전 달' in html
    assert '다음 달' in html


def test_homepage_popup(client, db):
    """Homepage should display active popups."""
    _seed_popup(title='테스트 팝업 공지', content='<p>팝업 내용입니다</p>')
    db.session.commit()

    resp = client.get('/')
    html = resp.data.decode()
    assert '테스트 팝업 공지' in html
    assert 'popup-overlay' in html


def test_homepage_no_inactive_popup(client, db):
    """Inactive popups should not appear."""
    _seed_popup(title='비활성 팝업', is_active=False)
    db.session.commit()

    resp = client.get('/')
    html = resp.data.decode()
    assert '비활성 팝업' not in html


# ---------------------------------------------------------------------------
# Static / Meta Tests
# ---------------------------------------------------------------------------

def test_robots_txt(client):
    """robots.txt should be accessible."""
    resp = client.get('/robots.txt')
    assert resp.status_code == 200
    assert b'User-agent' in resp.data


def test_sitemap_xml(client):
    """sitemap.xml should contain all URLs."""
    resp = client.get('/sitemap.xml')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert 'urlset' in html
    expected_urls = ['/about', '/teachers', '/programs', '/gallery',
                     '/notices', '/parent-notes', '/meals', '/events', '/contact']
    for url in expected_urls:
        assert url in html, f'Missing URL in sitemap: {url}'


def test_404_page(client):
    """404 page should render properly."""
    resp = client.get('/nonexistent-page')
    assert resp.status_code == 404


def test_no_invalid_html(client):
    """Homepage should not contain invalid HTML tags."""
    resp = client.get('/')
    html = resp.data.decode()
    assert '</br>' not in html, 'Found invalid </br> tag'
