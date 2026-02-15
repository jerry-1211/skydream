"""Pytest fixtures for test suite."""
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
    return app


@pytest.fixture(scope='session')
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """Fresh database for each test.

    Uses delete-all-rows instead of drop_all so that session-scoped
    fixtures (e.g. ``client``) still find tables after this teardown.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        # Delete all rows but keep tables intact for session-scoped client
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User(username='testadmin', is_admin=True)
    user.set_password('testpass123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_client(app, admin_user):
    """Authenticated test client."""
    client = app.test_client()
    with client:
        client.post('/auth/login', data={
            'username': 'testadmin',
            'password': 'testpass123',
        }, follow_redirects=True)
        yield client
