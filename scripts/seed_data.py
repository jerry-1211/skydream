#!/usr/bin/env python3
"""Seed the database with initial content from the original static site."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import SiteInfo, HeroSlide, Program, Gallery, Media, Teacher


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
    'principal_greeting': (
        '놀면서 자라고, 놀이는 곧 배움이 됩니다. '
        '공공형 어린이집은 놀이 중심의 보육을 실천하며 '
        '아이 스스로 탐색하고 경험하는 시간을 존중합니다.\n\n'
        '안정, 사랑, 즐거움이 조화를 이루는 공간 속에서 '
        '아이들이 마음껏 꿈꾸고 성장할 수 있도록 '
        '따뜻한 돌봄과 교육으로 함께 하겠습니다.'
    ),
    'curriculum_intro': '',
    'admission_info': '임신육아종합포털 아이사랑(www.childcare.go.kr)에서 온라인 신청 가능합니다.',
}

HERO_SLIDES_DATA = [
    {
        'heading': '아이들의 행복한 웃음이 가득한 곳',
        'description': '사랑과 전문성으로 아이들의 성장을 돕습니다.',
        'button_text': '입소 상담 문의하기',
        'button_link': '#contact',
        'sort_order': 1,
        'is_active': True,
        'image_filename': 'main1.png',
    },
    {
        'heading': '놀이중심 교육과정',
        'description': '아이들의 창의력과 꿈을 키우는 배움터',
        'button_text': '프로그램 보기',
        'button_link': '#programs',
        'sort_order': 2,
        'is_active': True,
        'image_filename': 'main2.png',
    },
    {
        'heading': '친구와 함께하는 즐거운 배움',
        'description': '소통하고 협력하며 함께 성장하는 공간',
        'button_text': '원운영안내',
        'button_link': '#info',
        'sort_order': 3,
        'is_active': True,
        'image_filename': 'main3.png',
    },
]

PROGRAMS_DATA = {
    'basic': [
        ('신비한 모험 놀이', '우주의 꿈을 키우는 아이들입니다.', 'basic1.png'),
        ('재미 쏙쏙 컵 쌓기 시간', '아이들의 공간 감각 능력을 길러봐요!', 'basic2.png'),
        ('줄을 맞춰 따라가기', '한 줄로 서서 기다리는 연습을 해봐요.', 'basic3.png'),
        ('다 함께 뛰어요', '바깥에서 맑은 공기를 마시며 자유롭게 뛰어놀아요.', 'basic4.png'),
        ('동물 체험', '동물 가면을 쓰고서 동물이 되어봐요!', 'basic5.png'),
        ('박스 꾸미기', '일상의 물건을 예쁘게 꾸며봅니다.', 'basic6.png'),
        ('깨끗이 씻어요', '더러워진 장난감을 스스로 씻어봅니다.', 'basic7.png'),
        ('요리 활동', '오감 톡톡! 쿠킹 플레이', 'basic8.png'),
        ('세차장 놀이', '반짝반짝 자동차 세차장이 열렸어요!', 'basic9.png'),
    ],
    'story': [
        (f'놀이이야기{i}', '', f'story{i}.png') for i in range(1, 10)
    ],
    'special': [
        ('동물병원 견학', '학부모님이 운영하는 동물병원 견학으로 아이의 꿈을 키워갑니다.', 'special1.png'),
        ('부모님 참여 수업', '참여해주시는 부모님께 감사의 마음을 담아 감사장을 드립니다.', 'special2.png'),
        ('크리스마스 활동', '크리스마스에 가족과 함께 맛있는 케이크를 만들어요!', 'special3.png'),
        ('어린이날 행사', '아이들을 위한 특별한 축제에 부모님도 함께 참여하세요.', 'special4.png'),
        ('현장 학습 체험', '아이들과 부모님이 함께하는 생생한 현장 학습 체험입니다.', 'special5.png'),
        ('가을 운동회', '아이들과 부모님이 함께하는 즐거운 가을 운동회에 참여하세요.', 'special6.png'),
        ('1일 교사', '오늘은 아빠가 선생님이 되어 직접 수업을 진행해요.', 'special7.png'),
    ],
    'action': [
        ('체육활동(중심 잡아요)', '발판에 올라가 균형 감각을 길러봅니다.', 'action1.png'),
        ('체육활동(다 함께 차차차)', '체육 선생님과 함께 신나게 운동해요!', 'action2.png'),
        ('체육활동(풍선 터널)', '풍선 터널을 통과하는 재미있는 놀이예요.', 'action3.png'),
        ('구멍으로 쏙!', '나만의 자리를 찾아 구멍으로 들어가요.', 'action4.png'),
        ('동물체험', '실제 동물들과 함께하는 생생한 체험이에요.', 'action5.png'),
        ('딸기 영어 체험(사랑해)', '친구들에게 사랑을 표현해봐요.', 'action6.png'),
        ('딸기 영어 체험(별자리 찾기)', '아이들의 별자리를 찾아봐요!', 'action7.png'),
        ('딸기 영어 체험(인형극)', '아이들에게 재미있는 인형극을 보여줘요.', 'action8.jpeg'),
    ],
    'act': [
        ('아이들과 자연이 만든 갤러리', '숲에서 아이들이 그린 멋진 작품입니다.', 'act1.jpeg'),
        ('동화같은 시간', '아이들과 부모님이 자연에서 보내는 소중한 시간이에요.', 'act2.png'),
        ('자연과 함께하는 하루', '아이들과 자연, 그리고 부모님의 행복한 시간이에요.', 'act3.png'),
        ('농장 체험', '직접 농작물을 수확하며 농장 체험을 해봐요.', 'act4.jpeg'),
        ('꼬마 농부', '아이들이 농부가 되는 특별한 체험이에요.', 'act5.png'),
        ('땅속에서 배우는 하루', '땅속에서 직접 캐서 음식의 소중함을 느껴봐요.', 'act6.png'),
        ('땅 속에서 꺼낸 선물', '직접 딴 수확물로 집에서 맛있게 먹어요.', 'act7.jpeg'),
    ],
}

GALLERY_DATA = [
    ('여름아 놀자', 'gallery_1.png'),
    ('인형극으로 전해요, 할머니의 사랑', 'gallery_2.png'),
    ('함께라서 더 빛나는 크리스마스', 'gallery_3.png'),
    ('흙공으로 하천을 구해요!', 'gallery_4.png'),
    ('여름 햇살 아래 함께 웃어요', 'gallery_5.png'),
    ('DMZ 평화 체험 놀이', 'gallery_6.png'),
    ('자식 농사 잘 지었네. 한가위 축제', 'gallery_7.jpeg'),
    ('코스모스 향기 따라 걷는 길', 'gallery_8.png'),
]

TEACHER_DATA = {
    'name': '원장',
    'title': '원장',
    'greeting': '놀면서 자라고, 놀이는 곧 배움이 됩니다.',
    'photo_filename': 'teacher.jpeg',
}


# ---------------------------------------------------------------------------
# Helper: determine file extension → type
# ---------------------------------------------------------------------------

def _file_type(filename):
    """Return 'image' for known image extensions."""
    return 'image'


def _file_size(filename, images_dir):
    """Return file size in bytes, or 0 if the file doesn't exist."""
    # filename may be in a subdirectory (e.g. basic/basic1.png) or root
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
        db.session.flush()  # get media.id

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

            # Image lives in a subdirectory named after the category
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


def clear_all_data():
    """Delete all seeded data (order matters for FK constraints)."""
    HeroSlide.query.delete()
    Program.query.delete()
    Gallery.query.delete()
    Teacher.query.delete()
    Media.query.delete()
    SiteInfo.query.delete()
    db.session.flush()
    print('  Cleared existing data.')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    app = create_app('development')

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

        db.session.commit()

        print()
        print('Database seeded successfully!')
        print(f'  - Site info: {SiteInfo.query.count()} entries')
        print(f'  - Media: {Media.query.count()} files')
        print(f'  - Hero slides: {HeroSlide.query.count()}')
        print(f'  - Programs: {Program.query.count()}')
        print(f'  - Gallery: {Gallery.query.count()}')
        print(f'  - Teachers: {Teacher.query.count()}')


if __name__ == '__main__':
    main()
