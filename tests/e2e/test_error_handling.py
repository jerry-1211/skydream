"""Test error handling."""


def test_404_returns_correct_status(client):
    """404 errors should return proper status code."""
    resp = client.get('/this-does-not-exist')
    assert resp.status_code == 404


def test_404_renders_template(client):
    """404 page should render user-friendly page."""
    resp = client.get('/this-does-not-exist')
    html = resp.data.decode()
    assert '404' in html or '찾을 수 없' in html


def test_health_endpoint(client):
    """Health endpoint should return 200."""
    resp = client.get('/health')
    assert resp.status_code == 200
