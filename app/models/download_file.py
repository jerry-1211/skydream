from datetime import datetime, timezone
from ..extensions import db


class DownloadFile(db.Model):
    __tablename__ = 'download_files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), default='')
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), default='')
    file_size = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<DownloadFile {self.title}>'

    @property
    def static_path(self):
        return f'uploads/downloads/{self.filename}'

    @property
    def file_extension(self):
        return self.filename.rsplit('.', 1)[-1].lower() if '.' in self.filename else ''

    @property
    def icon_class(self):
        ext = self.file_extension
        icons = {
            'pdf': 'fas fa-file-pdf',
            'doc': 'fas fa-file-word',
            'docx': 'fas fa-file-word',
            'xls': 'fas fa-file-excel',
            'xlsx': 'fas fa-file-excel',
            'ppt': 'fas fa-file-powerpoint',
            'pptx': 'fas fa-file-powerpoint',
            'hwp': 'fas fa-file-alt',
            'hwpx': 'fas fa-file-alt',
            'zip': 'fas fa-file-archive',
        }
        return icons.get(ext, 'fas fa-file')

    @property
    def icon_color(self):
        ext = self.file_extension
        colors = {
            'pdf': '#EF5350',
            'doc': '#42A5F5',
            'docx': '#42A5F5',
            'xls': '#66BB6A',
            'xlsx': '#66BB6A',
            'ppt': '#FF7043',
            'pptx': '#FF7043',
            'hwp': '#26C6DA',
            'hwpx': '#26C6DA',
        }
        return colors.get(ext, '#78909C')
