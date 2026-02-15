from ..extensions import db


class SiteInfo(db.Model):
    __tablename__ = 'site_info'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, default='')

    # Predefined keys
    KEYS = {
        'daycare_name': '어린이집 이름',
        'phone': '전화번호',
        'director_phone': '원장님 연락처',
        'address': '주소',
        'operating_hours': '운영시간',
        'extended_hours': '야간연장 운영시간',
        'closed_days': '휴원일',
        'principal_greeting': '원장님 인사말',
        'principal_greeting_2': '원장님 인사말 (2번째 문단)',
        'admission_info': '입소 안내',
        'capacity': '정원',
        'current_enrollment': '현원',
        'grade': '등급',
        'map_latitude': '지도 위도',
        'map_longitude': '지도 경도',
        'curriculum_intro': '교육과정 소개',
    }

    def __repr__(self):
        return f'<SiteInfo {self.key}={self.value[:30]}>'

    @classmethod
    def get_value(cls, key, default=''):
        info = cls.query.filter_by(key=key).first()
        return info.value if info else default

    @classmethod
    def set_value(cls, key, value):
        info = cls.query.filter_by(key=key).first()
        if info:
            info.value = value
        else:
            info = cls(key=key, value=value)
            from ..extensions import db
            db.session.add(info)
        return info
