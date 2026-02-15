"""Test public user navigation flow."""


def test_homepage_loads(client):
    """Homepage should return 200 and contain key sections."""
    resp = client.get('/')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '하늘 꿈나무 어린이집' in html
    assert 'hero' in html


def test_homepage_has_all_sections(client):
    """Homepage should contain all major sections."""
    resp = client.get('/')
    html = resp.data.decode()
    sections = ['hero', 'about', 'programs', 'gallery', 'info', 'contact']
    for section in sections:
        assert f'id="{section}"' in html, f'Missing section: {section}'


def test_homepage_has_navigation(client):
    """Homepage should have navigation links."""
    resp = client.get('/')
    html = resp.data.decode()
    nav_items = ['어린이집 소개', '배움과 놀이의 여정', '활동 앨범', '원운영안내', '오시는 길']
    for item in nav_items:
        assert item in html, f'Missing nav item: {item}'


def test_homepage_has_program_tabs(client):
    """Homepage should have all 5 program tabs."""
    resp = client.get('/')
    html = resp.data.decode()
    tabs = ['basic', 'story', 'special', 'action', 'act']
    for tab in tabs:
        assert f'data-tab="{tab}"' in html, f'Missing tab: {tab}'


def test_homepage_has_program_cards(client):
    """Homepage should have 40 program cards."""
    resp = client.get('/')
    html = resp.data.decode()
    count = html.count('program-card')
    assert count == 40, f'Expected 40 program cards, got {count}'


def test_homepage_has_gallery_items(client):
    """Homepage should have 8 gallery items."""
    resp = client.get('/')
    html = resp.data.decode()
    count = html.count('gallery-item')
    assert count == 8, f'Expected 8 gallery items, got {count}'


def test_homepage_has_info_tabs(client):
    """Homepage should have admission, schedule, meal tabs."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'data-tab="admission"' in html
    assert 'data-tab="schedule"' in html
    assert 'data-tab="meal"' in html


def test_homepage_has_contact_info(client):
    """Homepage should have contact information."""
    resp = client.get('/')
    html = resp.data.decode()
    assert '031-818-9150' in html
    assert '중산동' in html


def test_homepage_has_google_maps(client):
    """Homepage should have Google Maps embed."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'maps.google.com' in html


def test_robots_txt(client):
    """robots.txt should be accessible."""
    resp = client.get('/robots.txt')
    assert resp.status_code == 200
    assert b'User-agent' in resp.data


def test_sitemap_xml(client):
    """sitemap.xml should be accessible."""
    resp = client.get('/sitemap.xml')
    assert resp.status_code == 200
    assert b'urlset' in resp.data


def test_404_page(client):
    """404 page should render properly."""
    resp = client.get('/nonexistent-page')
    assert resp.status_code == 404


def test_no_invalid_html(client):
    """Homepage should not contain invalid HTML tags."""
    resp = client.get('/')
    html = resp.data.decode()
    assert '</br>' not in html, 'Found invalid </br> tag'
