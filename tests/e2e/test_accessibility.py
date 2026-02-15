"""Test accessibility features."""


def test_has_lang_attribute(client):
    """HTML should have lang='ko' attribute."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'lang="ko"' in html


def test_has_skip_navigation(client):
    """Page should have skip-to-content link."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'skip-to-content' in html
    assert 'main-content' in html


def test_has_aria_landmarks(client):
    """Page should have ARIA landmark roles."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'role="banner"' in html
    assert 'role="main"' in html
    assert 'role="contentinfo"' in html


def test_has_aria_navigation(client):
    """Navigation should have ARIA attributes."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'aria-label' in html


def test_images_have_alt_text(client):
    """All images should have alt attributes."""
    resp = client.get('/')
    html = resp.data.decode()
    # Count img tags vs img tags with alt
    import re
    imgs = re.findall(r'<img[^>]*>', html)
    for img in imgs:
        assert 'alt=' in img, f'Image missing alt attribute: {img[:80]}'


def test_has_meta_description(client):
    """Page should have meta description."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'meta name="description"' in html or 'name="description"' in html


def test_has_structured_data(client):
    """Page should have Schema.org structured data."""
    resp = client.get('/')
    html = resp.data.decode()
    assert 'schema.org' in html
    assert 'ChildCare' in html
