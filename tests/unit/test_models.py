"""Test database models."""
import pytest
from app.models import User, Notice, SiteInfo, Program, Media


class TestUserModel:
    def test_password_hashing(self, db):
        user = User(username='test')
        user.set_password('password123')
        assert user.check_password('password123')
        assert not user.check_password('wrong')

    def test_user_repr(self, db):
        user = User(username='testuser')
        assert 'testuser' in repr(user)


class TestNoticeModel:
    def test_create_notice(self, db):
        notice = Notice(title='Test', content='Content')
        db.session.add(notice)
        db.session.commit()
        assert notice.id is not None
        assert notice.created_at is not None


class TestSiteInfoModel:
    def test_get_set_value(self, db):
        SiteInfo.set_value('phone', '031-818-9150')
        db.session.commit()
        assert SiteInfo.get_value('phone') == '031-818-9150'

    def test_get_default(self, db):
        val = SiteInfo.get_value('nonexistent', 'default')
        assert val == 'default'


class TestProgramModel:
    def test_categories(self):
        assert 'basic' in Program.CATEGORIES
        assert 'story' in Program.CATEGORIES
