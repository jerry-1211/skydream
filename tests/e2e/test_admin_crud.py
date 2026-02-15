"""Test admin CRUD operations."""
import pytest
from app.models import Notice, Program, Gallery, Event, Teacher, MealPlan, ParentNote, HeroSlide
from app.extensions import db as _db


class TestAdminAccess:
    """Test admin authentication and access."""

    def test_admin_requires_login(self, client):
        """Admin pages should redirect to login."""
        resp = client.get('/admin/')
        assert resp.status_code == 302
        assert '/auth/login' in resp.headers.get('Location', '')

    def test_login_page_loads(self, client):
        """Login page should load."""
        resp = client.get('/auth/login')
        assert resp.status_code == 200

    def test_admin_dashboard_after_login(self, auth_client):
        """Dashboard should load after authentication."""
        resp = auth_client.get('/admin/')
        assert resp.status_code == 200
        html = resp.data.decode()
        assert '대시보드' in html


class TestNoticesCRUD:
    """Test notice CRUD operations."""

    def test_notices_list(self, auth_client):
        resp = auth_client.get('/admin/notices/')
        assert resp.status_code == 200

    def test_notices_create_page(self, auth_client):
        resp = auth_client.get('/admin/notices/create')
        assert resp.status_code == 200

    def test_notices_create(self, auth_client, db):
        resp = auth_client.post('/admin/notices/create', data={
            'title': '테스트 공지',
            'content': '테스트 내용입니다.',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert Notice.query.filter_by(title='테스트 공지').first() is not None


class TestProgramsCRUD:
    """Test program CRUD operations."""

    def test_programs_list(self, auth_client):
        resp = auth_client.get('/admin/programs/')
        assert resp.status_code == 200

    def test_programs_create_page(self, auth_client):
        resp = auth_client.get('/admin/programs/create')
        assert resp.status_code == 200


class TestGalleryCRUD:
    """Test gallery CRUD operations."""

    def test_gallery_list(self, auth_client):
        resp = auth_client.get('/admin/gallery/')
        assert resp.status_code == 200


class TestMediaManagement:
    """Test media management."""

    def test_media_list(self, auth_client):
        resp = auth_client.get('/admin/media/')
        assert resp.status_code == 200

    def test_media_upload_page(self, auth_client):
        resp = auth_client.get('/admin/media/upload')
        assert resp.status_code == 200


class TestSiteInfo:
    """Test site info management."""

    def test_site_info_page(self, auth_client):
        resp = auth_client.get('/admin/site-info/')
        assert resp.status_code == 200


class TestMealsCRUD:
    def test_meals_list(self, auth_client):
        resp = auth_client.get('/admin/meals/')
        assert resp.status_code == 200


class TestEventsCRUD:
    def test_events_list(self, auth_client):
        resp = auth_client.get('/admin/events/')
        assert resp.status_code == 200


class TestTeachersCRUD:
    def test_teachers_list(self, auth_client):
        resp = auth_client.get('/admin/teachers/')
        assert resp.status_code == 200


class TestParentNotesCRUD:
    def test_parent_notes_list(self, auth_client):
        resp = auth_client.get('/admin/parent-notes/')
        assert resp.status_code == 200


class TestHeroSlidesCRUD:
    def test_hero_slides_list(self, auth_client):
        resp = auth_client.get('/admin/hero-slides/')
        assert resp.status_code == 200
