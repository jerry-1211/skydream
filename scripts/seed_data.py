#!/usr/bin/env python3
"""Seed the database with initial content from the original static site."""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import SiteInfo, HeroSlide, Program, Gallery, Media, Teacher, Notice, Event, MealPlan, ParentNote, Popup, DailySchedule


# ---------------------------------------------------------------------------
# Data definitions
# ---------------------------------------------------------------------------

SITE_INFO_DATA = {
    'daycare_name': '공공형 하늘 꿈나무 어린이집',
    'phone': '031-818-9150',
    'director_phone': '010-5058-0771',
    'address': '경기 고양시 일산동구 중산동 1800',
    'operating_hours': '07:30 ~ 19:30',
    'extended_hours': '19:30 ~ 21:30',
    'closed_days': '일요일, 공휴일',
    'capacity': '20명',
    'grade': 'A등급 공공형 어린이집',
    'map_latitude': '37.6770705',
    'map_longitude': '126.787819',
    'principal_greeting': '안녕하세요, 학부모님! 놀면서 자라고, 놀이는 곧 배움이 됩니다. 하늘 꿈나무 어린이집은 놀이 중심의 보육을 실천하며 아이 스스로 탐색하고 경험하는 시간을 소중히 여깁니다.',
    'principal_greeting_2': '안정, 사랑, 즐거움이 조화를 이루는 공간 속에서 아이들이 마음껏 꿈꾸고 성장할 수 있도록 엄마의 마음으로 따뜻하게 돌보겠습니다.',
    'curriculum_intro': '',
    'admission_info': '임신육아종합포털 아이사랑(www.childcare.go.kr)에서 온라인 신청 가능합니다.',
    'admission_details': '만 0세~2세 영아 보육\n공공형 어린이집 우선순위 적용\n입소 상담 후 최종 결정\n정원: 20명',
    'meal_features': '저염식 인증 어린이집\n신선한 제철 식재료 사용\n아워홈 식재료 공급업체\n알레르기 대응 개별 식단\n영양사 관리 하의 균형 잡힌 식사',
}

HERO_SLIDES_DATA = [
    {
        'heading': '아이들의 행복한 웃음이 가득한 곳',
        'description': '사랑과 전문성으로 아이들의 성장을 돕습니다.',
        'button_text': '입소 상담 문의하기',
        'button_link': '/contact',
        'sort_order': 1,
        'is_active': True,
        'image_filename': 'main1.jpg',
    },
    {
        'heading': '놀이중심 교육과정',
        'description': '아이들의 창의력과 꿈을 키우는 배움터',
        'button_text': '프로그램 보기',
        'button_link': '/programs',
        'sort_order': 2,
        'is_active': True,
        'image_filename': 'main2.jpg',
    },
    {
        'heading': '친구와 함께하는 즐거운 배움',
        'description': '소통하고 협력하며 함께 성장하는 공간',
        'button_text': '어린이집 소개',
        'button_link': '/about',
        'sort_order': 3,
        'is_active': True,
        'image_filename': 'main3.jpg',
    },
]

PROGRAMS_DATA = {
    'basic': [
        ('신비한 모험 놀이', '우주의 꿈을 키우는 아이들입니다.', 'basic1.jpg'),
        ('재미 쏙쏙 컵 쌓기 시간', '아이들의 공간 감각 능력을 길러봐요!', 'basic2.jpg'),
        ('줄을 맞춰 따라가기', '한 줄로 서서 기다리는 연습을 해봐요.', 'basic3.jpg'),
        ('다 함께 뛰어요', '바깥에서 맑은 공기를 마시며 자유롭게 뛰어놀아요.', 'basic4.jpg'),
        ('동물 체험', '동물 가면을 쓰고서 동물이 되어봐요!', 'basic5.jpg'),
        ('박스 꾸미기', '일상의 물건을 예쁘게 꾸며봅니다.', 'basic6.jpg'),
        ('깨끗이 씻어요', '더러워진 장난감을 스스로 씻어봅니다.', 'basic7.jpg'),
        ('요리 활동', '오감 톡톡! 쿠킹 플레이', 'basic8.jpg'),
        ('세차장 놀이', '반짝반짝 자동차 세차장이 열렸어요!', 'basic9.jpg'),
    ],
    'story': [
        (f'놀이이야기{i}', '', f'story{i}.jpg') for i in range(1, 10)
    ],
    'special': [
        ('동물병원 견학', '학부모님이 운영하는 동물병원 견학으로 아이의 꿈을 키워갑니다.', 'special1.jpg'),
        ('부모님 참여 수업', '참여해주시는 부모님께 감사의 마음을 담아 감사장을 드립니다.', 'special2.jpg'),
        ('크리스마스 활동', '크리스마스에 가족과 함께 맛있는 케이크를 만들어요!', 'special3.jpg'),
        ('어린이날 행사', '아이들을 위한 특별한 축제에 부모님도 함께 참여하세요.', 'special4.jpg'),
        ('현장 학습 체험', '아이들과 부모님이 함께하는 생생한 현장 학습 체험입니다.', 'special5.jpg'),
        ('가을 운동회', '아이들과 부모님이 함께하는 즐거운 가을 운동회에 참여하세요.', 'special6.jpg'),
        ('1일 교사', '오늘은 아빠가 선생님이 되어 직접 수업을 진행해요.', 'special7.jpg'),
    ],
    'action': [
        ('체육활동(중심 잡아요)', '발판에 올라가 균형 감각을 길러봅니다.', 'action1.jpg'),
        ('체육활동(다 함께 차차차)', '체육 선생님과 함께 신나게 운동해요!', 'action2.jpg'),
        ('체육활동(풍선 터널)', '풍선 터널을 통과하는 재미있는 놀이예요.', 'action3.jpg'),
        ('구멍으로 쏙!', '나만의 자리를 찾아 구멍으로 들어가요.', 'action4.jpg'),
        ('동물체험', '실제 동물들과 함께하는 생생한 체험이에요.', 'action5.jpg'),
        ('딸기 영어 체험(사랑해)', '친구들에게 사랑을 표현해봐요.', 'action6.jpg'),
        ('딸기 영어 체험(별자리 찾기)', '아이들의 별자리를 찾아봐요!', 'action7.jpg'),
        ('딸기 영어 체험(인형극)', '아이들에게 재미있는 인형극을 보여줘요.', 'action8.jpg'),
    ],
    'act': [
        ('아이들과 자연이 만든 갤러리', '숲에서 아이들이 그린 멋진 작품입니다.', 'act1.jpg'),
        ('동화같은 시간', '아이들과 부모님이 자연에서 보내는 소중한 시간이에요.', 'act2.jpg'),
        ('자연과 함께하는 하루', '아이들과 자연, 그리고 부모님의 행복한 시간이에요.', 'act3.jpg'),
        ('농장 체험', '직접 농작물을 수확하며 농장 체험을 해봐요.', 'act4.jpg'),
        ('꼬마 농부', '아이들이 농부가 되는 특별한 체험이에요.', 'act5.jpg'),
        ('땅속에서 배우는 하루', '땅속에서 직접 캐서 음식의 소중함을 느껴봐요.', 'act6.jpg'),
        ('땅 속에서 꺼낸 선물', '직접 딴 수확물로 집에서 맛있게 먹어요.', 'act7.jpg'),
    ],
}

GALLERY_DATA = [
    ('여름아 놀자', 'gallery_1.jpg'),
    ('인형극으로 전해요, 할머니의 사랑', 'gallery_2.jpg'),
    ('함께라서 더 빛나는 크리스마스', 'gallery_3.jpg'),
    ('흙공으로 하천을 구해요!', 'gallery_4.jpg'),
    ('여름 햇살 아래 함께 웃어요', 'gallery_5.jpg'),
    ('DMZ 평화 체험 놀이', 'gallery_6.jpg'),
    ('자식 농사 잘 지었네. 한가위 축제', 'gallery_7.jpg'),
    ('코스모스 향기 따라 걷는 길', 'gallery_8.jpg'),
]

TEACHER_DATA = {
    'name': '원장',
    'title': '원장',
    'greeting': '놀면서 자라고, 놀이는 곧 배움이 됩니다.',
    'photo_filename': 'teacher.jpg',
}

NOTICES_DATA = [
    {
        'title': '2026년 봄학기 신규 원아 모집 안내',
        'content': '2026년 봄학기 신규 원아를 모집합니다.\n\n모집 대상: 만 0세~2세\n모집 인원: 약간 명\n접수 기간: 2026년 2월 1일 ~ 2월 28일\n접수 방법: 아이사랑 포털(www.childcare.go.kr) 온라인 접수\n\n문의: 031-818-9150',
        'is_pinned': True,
    },
    {
        'title': '2월 보육료 납부 안내',
        'content': '2월 보육료 납부 기간을 안내드립니다.\n\n납부 기간: 2026년 2월 1일 ~ 2월 10일\n납부 방법: 아이행복카드 자동결제\n\n궁금한 사항은 어린이집으로 문의해 주세요.',
        'is_pinned': False,
    },
    {
        'title': '설날 연휴 휴원 안내',
        'content': '설날 연휴 기간 동안 어린이집이 휴원합니다.\n\n휴원 기간: 2026년 2월 16일(월) ~ 2월 18일(수)\n정상 운영: 2026년 2월 19일(목)부터\n\n즐거운 명절 보내세요!',
        'is_pinned': False,
    },
    {
        'title': '겨울철 건강관리 안내',
        'content': '겨울철 감기 예방을 위한 건강관리 수칙을 안내합니다.\n\n1. 외출 후 손 씻기를 철저히 해주세요.\n2. 실내 적정 온도(20~22도)와 습도(50~60%)를 유지해 주세요.\n3. 균형 잡힌 식사와 충분한 수면이 중요합니다.\n4. 증상이 있을 경우 등원을 자제해 주세요.',
        'is_pinned': False,
    },
    {
        'title': '어린이집 안전교육 실시 안내',
        'content': '정기 안전교육을 실시합니다.\n\n일시: 2026년 2월 25일(화) 오전 10시\n내용: 화재 대피 훈련 및 교통안전 교육\n대상: 전체 원아\n\n안전한 어린이집을 위해 항상 노력하겠습니다.',
        'is_pinned': False,
    },
]

EVENTS_DATA = [
    {
        'title': '설날맞이 전통놀이 행사',
        'description': '우리 전통 놀이를 체험하며 설날의 의미를 배워요.',
        'event_date': date(2026, 2, 14),
        'event_type': 'special',
    },
    {
        'title': '겨울 현장학습 - 눈썰매장',
        'description': '친구들과 함께 눈썰매장에서 신나는 겨울을 즐겨요.',
        'event_date': date(2026, 2, 20),
        'event_type': 'field_trip',
    },
    {
        'title': '2월 학부모 상담 주간',
        'description': '학부모님과 담임 교사의 1:1 상담이 진행됩니다.',
        'event_date': date(2026, 2, 24),
        'event_type': 'parent',
    },
    {
        'title': '3월 개학식',
        'description': '새 학기를 맞이하는 개학식을 진행합니다.',
        'event_date': date(2026, 3, 2),
        'event_type': 'general',
    },
    {
        'title': '봄맞이 식목일 행사',
        'description': '아이들이 직접 작은 화분에 씨앗을 심어요.',
        'event_date': date(2026, 3, 12),
        'event_type': 'special',
    },
    {
        'title': '3월 생일잔치',
        'description': '3월에 태어난 친구들의 생일을 축하해요!',
        'event_date': date(2026, 3, 20),
        'event_type': 'general',
    },
]

MEAL_DATA = []
_meal_week_start = date(2026, 2, 16)
_menus = {
    0: {  # Monday
        'breakfast': ['흰밥', '미역국', '계란말이', '깍두기'],
        'lunch': ['잡곡밥', '된장찌개', '소고기불고기', '나물무침', '배추김치'],
        'snack': ['우유', '과일(사과)'],
    },
    1: {  # Tuesday
        'breakfast': ['흰밥', '콩나물국', '김구이', '깍두기'],
        'lunch': ['흰밥', '어묵탕', '닭갈비', '감자조림', '배추김치'],
        'snack': ['요구르트', '고구마'],
    },
    2: {  # Wednesday
        'breakfast': ['흰밥', '시금치국', '두부조림', '깍두기'],
        'lunch': ['카레라이스', '미니돈까스', '양배추샐러드', '배추김치'],
        'snack': ['우유', '떡볶이'],
    },
    3: {  # Thursday
        'breakfast': ['흰밥', '감자국', '멸치볶음', '깍두기'],
        'lunch': ['잡곡밥', '김치찌개', '생선구이', '콩나물무침', '배추김치'],
        'snack': ['주스', '과일(바나나)'],
    },
    4: {  # Friday
        'breakfast': ['흰밥', '무국', '햄야채볶음', '깍두기'],
        'lunch': ['비빔밥', '콩나물국', '배추김치'],
        'snack': ['우유', '쿠키'],
    },
}
for day_offset in range(5):
    plan_date = _meal_week_start + timedelta(days=day_offset)
    day_menus = _menus.get(day_offset, {})
    for meal_type, items in day_menus.items():
        MEAL_DATA.append({
            'plan_date': plan_date,
            'meal_type': meal_type,
            'menu_items': items,
        })

PARENT_NOTES_DATA = [
    {
        'title': '2월 가정통신문 - 겨울철 건강관리',
        'content': '안녕하세요, 하늘 꿈나무 어린이집입니다.\n\n겨울철 건강관리에 대해 안내드립니다.\n\n1. 충분한 수분 섭취를 해주세요.\n2. 외출 시 따뜻하게 옷을 입혀주세요.\n3. 손 씻기를 생활화해 주세요.\n\n감사합니다.',
        'target_class': 'all',
    },
    {
        'title': '0세반 적응 프로그램 안내',
        'content': '0세반 신입 원아 적응 프로그램을 안내드립니다.\n\n기간: 입소 후 2주간\n방법: 단계적으로 보육 시간을 늘려갑니다.\n\n1일차~3일차: 오전 2시간 (보호자 동반)\n4일차~7일차: 오전 반일\n8일차~14일차: 종일반\n\n아이의 적응 상태에 따라 기간이 조정될 수 있습니다.',
        'target_class': 'age0',
    },
    {
        'title': '1세반 2월 활동 계획안',
        'content': '1세반 2월 활동 계획을 안내드립니다.\n\n주제: 겨울과 우리\n\n1주: 겨울 날씨 느끼기\n2주: 따뜻하게 입어요\n3주: 겨울 놀이\n4주: 설날 놀이\n\n가정에서도 관련 활동을 해보시면 좋겠습니다.',
        'target_class': 'age1',
    },
    {
        'title': '2세반 졸업식 안내',
        'content': '2세반 졸업식 일정을 안내드립니다.\n\n일시: 2026년 2월 28일(토) 오전 11시\n장소: 어린이집 놀이실\n\n보호자 참석을 부탁드립니다.\n준비물: 없음 (졸업앨범은 어린이집에서 준비합니다)\n\n졸업을 진심으로 축하합니다!',
        'target_class': 'age2',
    },
]

POPUP_DATA = [
    {
        'title': '2026년 봄학기 원아 모집',
        'content': '<p style="text-align:center;font-size:1.1rem;"><strong>2026년 봄학기 원아 모집중!</strong></p><p style="text-align:center;">자세한 사항은 전화문의 바랍니다.</p><p style="text-align:center;">☎ 031-818-9150</p>',
        'link_url': '/contact',
        'is_active': True,
        'show_today_hide': True,
        'position': 'center',
        'width': 440,
        'sort_order': 1,
    },
    {
        'title': '통학버스 운영 안내',
        'content': (
            '<div style="text-align:center; padding: 10px;">'
            '<p style="font-size:1.2rem; font-weight:bold; color:#2c5282; margin-bottom:12px;">🚌 통학버스 운영 안내</p>'
            '<p style="font-size:0.95rem; margin-bottom:8px;">하늘 꿈나무 어린이집에서<br><strong>통학버스를 운영</strong>합니다.</p>'
            '<hr style="border:none; border-top:1px solid #e2e8f0; margin:12px 0;">'
            '<p style="font-size:0.9rem; line-height:1.8; text-align:left; padding:0 10px;">'
            '🕗 <strong>등원</strong>: 오전 8:00 ~ 9:00<br>'
            '🕓 <strong>하원</strong>: 오후 4:00 ~ 5:00<br>'
            '📍 <strong>운행 구간</strong>: 중산동, 풍산동, 백석동 일대<br>'
            '💰 <strong>이용료</strong>: 월 50,000원'
            '</p>'
            '<hr style="border:none; border-top:1px solid #e2e8f0; margin:12px 0;">'
            '<p style="font-size:0.9rem;">문의: <strong>031-818-9150</strong></p>'
            '</div>'
        ),
        'link_url': '/contact',
        'is_active': True,
        'show_today_hide': True,
        'position': 'center',
        'width': 420,
        'sort_order': 2,
    },
]

DAILY_SCHEDULE_DATA = [
    {'time_label': '07:30', 'icon_class': 'fas fa-sun', 'title': '등원 및 맞이', 'description': '반갑게 인사하고 건강 관찰, 자유놀이', 'sort_order': 1},
    {'time_label': '09:30', 'icon_class': 'fas fa-apple-alt', 'title': '오전 간식', 'description': '영양 가득한 과일과 간식 시간', 'sort_order': 2},
    {'time_label': '10:00', 'icon_class': 'fas fa-book-reader', 'title': '놀이 활동', 'description': '표준보육과정에 따른 놀이 중심 수업', 'sort_order': 3},
    {'time_label': '11:30', 'icon_class': 'fas fa-utensils', 'title': '점심 식사', 'description': '영양사가 관리하는 균형 잡힌 점심', 'sort_order': 4},
    {'time_label': '12:30', 'icon_class': 'fas fa-cloud-moon', 'title': '낮잠', 'description': '편안한 환경에서 달콤한 낮잠 시간', 'sort_order': 5},
    {'time_label': '15:00', 'icon_class': 'fas fa-cookie-bite', 'title': '오후 간식 & 놀이', 'description': '간식 후 실내외 자유놀이 활동', 'sort_order': 6},
    {'time_label': '16:30', 'icon_class': 'fas fa-hand-wave', 'title': '하원', 'description': '하루 이야기 나누고 안전하게 귀가', 'sort_order': 7},
]


# ---------------------------------------------------------------------------
# Helper: determine file extension -> type
# ---------------------------------------------------------------------------

def _file_type(filename):
    """Return 'image' for known image extensions."""
    return 'image'


def _file_size(filename, images_dir):
    """Return file size in bytes, or 0 if the file doesn't exist."""
    path = os.path.join(images_dir, filename)
    if os.path.isfile(path):
        return os.path.getsize(path)
    return 0


def _create_media(filename, category, alt_text, images_dir):
    """Create and return a Media record (not yet committed)."""
    media = Media(
        filename=filename,
        original_filename=filename,
        file_type=_file_type(filename),
        file_size=_file_size(filename, images_dir),
        alt_text=alt_text,
        category=category,
    )
    db.session.add(media)
    return media


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

def seed_site_info():
    """Seed site information key-value pairs."""
    count = 0
    for key, value in SITE_INFO_DATA.items():
        existing = SiteInfo.query.filter_by(key=key).first()
        if not existing:
            db.session.add(SiteInfo(key=key, value=value))
            count += 1
    db.session.flush()
    print(f'  Site info: {count} new entries added.')


def seed_hero_slides(images_dir):
    """Seed hero slides with associated media."""
    count = 0
    for slide_data in HERO_SLIDES_DATA:
        existing = HeroSlide.query.filter_by(heading=slide_data['heading']).first()
        if existing:
            continue

        image_filename = slide_data['image_filename']
        media = _create_media(image_filename, 'hero', slide_data['heading'], images_dir)
        db.session.flush()

        slide = HeroSlide(
            heading=slide_data['heading'],
            description=slide_data['description'],
            button_text=slide_data['button_text'],
            button_link=slide_data['button_link'],
            image_id=media.id,
            sort_order=slide_data['sort_order'],
            is_active=slide_data['is_active'],
        )
        db.session.add(slide)
        count += 1
    db.session.flush()
    print(f'  Hero slides: {count} new slides added.')


def seed_programs(images_dir):
    """Seed program cards with associated media."""
    count = 0
    for category, items in PROGRAMS_DATA.items():
        for sort_idx, (title, description, image_filename) in enumerate(items, start=1):
            existing = Program.query.filter_by(category=category, title=title).first()
            if existing:
                continue

            image_path = f'{category}/{image_filename}'
            media = _create_media(image_path, 'program', title, images_dir)
            db.session.flush()

            program = Program(
                category=category,
                title=title,
                description=description,
                image_id=media.id,
                sort_order=sort_idx,
            )
            db.session.add(program)
            count += 1
    db.session.flush()
    print(f'  Programs: {count} new cards added.')


def seed_gallery(images_dir):
    """Seed gallery items with associated media."""
    count = 0
    for sort_idx, (title, image_filename) in enumerate(GALLERY_DATA, start=1):
        existing = Gallery.query.filter_by(title=title).first()
        if existing:
            continue

        media = _create_media(image_filename, 'gallery', title, images_dir)
        db.session.flush()

        gallery = Gallery(
            title=title,
            image_id=media.id,
            sort_order=sort_idx,
        )
        db.session.add(gallery)
        count += 1
    db.session.flush()
    print(f'  Gallery: {count} new items added.')


def seed_teachers(images_dir):
    """Seed teacher records with associated media."""
    data = TEACHER_DATA
    existing = Teacher.query.filter_by(name=data['name']).first()
    if existing:
        print('  Teachers: already seeded.')
        return

    media = _create_media(data['photo_filename'], 'teacher', data['name'], images_dir)
    db.session.flush()

    teacher = Teacher(
        name=data['name'],
        title=data['title'],
        greeting=data['greeting'],
        photo_id=media.id,
        sort_order=1,
    )
    db.session.add(teacher)
    db.session.flush()
    print('  Teachers: 1 new teacher added.')


def seed_notices():
    """Seed notice entries."""
    count = 0
    for notice_data in NOTICES_DATA:
        existing = Notice.query.filter_by(title=notice_data['title']).first()
        if existing:
            continue
        notice = Notice(
            title=notice_data['title'],
            content=notice_data['content'],
            is_pinned=notice_data['is_pinned'],
        )
        db.session.add(notice)
        count += 1
    db.session.flush()
    print(f'  Notices: {count} new notices added.')


def seed_events():
    """Seed event entries."""
    count = 0
    for event_data in EVENTS_DATA:
        existing = Event.query.filter_by(title=event_data['title']).first()
        if existing:
            continue
        event = Event(
            title=event_data['title'],
            description=event_data['description'],
            event_date=event_data['event_date'],
            event_type=event_data['event_type'],
        )
        db.session.add(event)
        count += 1
    db.session.flush()
    print(f'  Events: {count} new events added.')


def seed_meals():
    """Seed meal plan entries for one week."""
    count = 0
    for meal_data in MEAL_DATA:
        existing = MealPlan.query.filter_by(
            plan_date=meal_data['plan_date'],
            meal_type=meal_data['meal_type']
        ).first()
        if existing:
            continue
        meal = MealPlan(
            plan_date=meal_data['plan_date'],
            meal_type=meal_data['meal_type'],
        )
        meal.menu_items = meal_data['menu_items']
        db.session.add(meal)
        count += 1
    db.session.flush()
    print(f'  Meals: {count} new meal plans added.')


def seed_parent_notes():
    """Seed parent note entries."""
    count = 0
    for note_data in PARENT_NOTES_DATA:
        existing = ParentNote.query.filter_by(title=note_data['title']).first()
        if existing:
            continue
        note = ParentNote(
            title=note_data['title'],
            content=note_data['content'],
            target_class=note_data['target_class'],
        )
        db.session.add(note)
        count += 1
    db.session.flush()
    print(f'  Parent notes: {count} new notes added.')


def seed_popups():
    """Seed popup entries."""
    count = 0
    for popup_data in POPUP_DATA:
        existing = Popup.query.filter_by(title=popup_data['title']).first()
        if existing:
            continue
        popup = Popup(
            title=popup_data['title'],
            content=popup_data['content'],
            link_url=popup_data.get('link_url', ''),
            is_active=popup_data.get('is_active', True),
            show_today_hide=popup_data.get('show_today_hide', True),
            position=popup_data.get('position', 'center'),
            width=popup_data.get('width', 480),
            sort_order=popup_data.get('sort_order', 0),
        )
        db.session.add(popup)
        count += 1
    db.session.flush()
    print(f'  Popups: {count} new popups added.')


def seed_daily_schedule():
    """Seed daily schedule entries."""
    count = 0
    for item_data in DAILY_SCHEDULE_DATA:
        existing = DailySchedule.query.filter_by(
            time_label=item_data['time_label'],
            title=item_data['title']
        ).first()
        if existing:
            continue
        item = DailySchedule(
            time_label=item_data['time_label'],
            icon_class=item_data['icon_class'],
            title=item_data['title'],
            description=item_data['description'],
            sort_order=item_data['sort_order'],
        )
        db.session.add(item)
        count += 1
    db.session.flush()
    print(f'  Daily schedule: {count} new items added.')


def clear_all_data():
    """Delete all seeded data (order matters for FK constraints)."""
    HeroSlide.query.delete()
    Program.query.delete()
    Gallery.query.delete()
    Teacher.query.delete()
    Notice.query.delete()
    Event.query.delete()
    MealPlan.query.delete()
    ParentNote.query.delete()
    Popup.query.delete()
    DailySchedule.query.delete()
    Media.query.delete()
    SiteInfo.query.delete()
    db.session.flush()
    print('  Cleared existing data.')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    env = os.environ.get('FLASK_ENV', 'development')
    config_name = 'production' if env == 'production' else 'development'
    app = create_app(config_name)

    with app.app_context():
        db.create_all()

        # Determine the images directory
        images_dir = os.path.join(app.static_folder, 'images')

        # Check if already seeded
        if SiteInfo.query.first():
            if '--force' not in sys.argv:
                print('Database already seeded. Use --force to re-seed.')
                return
            print('Re-seeding database (--force)...')
            clear_all_data()

        print('Seeding database...')
        seed_site_info()
        seed_hero_slides(images_dir)
        seed_programs(images_dir)
        seed_gallery(images_dir)
        seed_teachers(images_dir)
        seed_notices()
        seed_events()
        seed_meals()
        seed_parent_notes()
        seed_popups()
        seed_daily_schedule()

        db.session.commit()

        print()
        print('Database seeded successfully!')
        print(f'  - Site info: {SiteInfo.query.count()} entries')
        print(f'  - Media: {Media.query.count()} files')
        print(f'  - Hero slides: {HeroSlide.query.count()}')
        print(f'  - Programs: {Program.query.count()}')
        print(f'  - Gallery: {Gallery.query.count()}')
        print(f'  - Teachers: {Teacher.query.count()}')
        print(f'  - Notices: {Notice.query.count()}')
        print(f'  - Events: {Event.query.count()}')
        print(f'  - Meals: {MealPlan.query.count()}')
        print(f'  - Parent notes: {ParentNote.query.count()}')
        print(f'  - Popups: {Popup.query.count()}')
        print(f'  - Daily schedule: {DailySchedule.query.count()}')


if __name__ == '__main__':
    main()
