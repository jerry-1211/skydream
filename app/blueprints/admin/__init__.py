from flask import Blueprint
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def require_login():
    """All admin routes require authentication."""
    pass


# Import routes after blueprint creation to avoid circular imports
from . import dashboard, notices, media, programs, gallery, hero_slides, site_info, meals, events, teachers, parent_notes, popups, daily_schedule, download_files  # noqa: E402, F401
