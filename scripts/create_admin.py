#!/usr/bin/env python3
"""Create an admin user for the daycare website."""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User


def create_admin():
    app = create_app()

    with app.app_context():
        db.create_all()

        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'changeme')

        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f'Admin user "{username}" already exists. Updating password.')
            existing.set_password(password)
        else:
            user = User(username=username, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            print(f'Admin user "{username}" created successfully.')

        db.session.commit()
        print('Done.')


if __name__ == '__main__':
    create_admin()
