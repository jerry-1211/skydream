"""하늘 꿈나무 어린이집 OG 이미지 생성 스크립트"""
from PIL import Image, ImageDraw, ImageFont
import os

def generate_og_image():
    """600x600 OG 이미지 생성 (하늘색 배경 + 어린이집 이름)"""
    width, height = 600, 600
    img = Image.new('RGB', (width, height), '#E3F2FD')
    draw = ImageDraw.Draw(img)

    # 구름 그리기
    cloud_color = '#90CAF9'
    draw.ellipse([120, 180, 300, 320], fill=cloud_color)
    draw.ellipse([200, 150, 400, 310], fill='#64B5F6')
    draw.ellipse([300, 170, 460, 330], fill=cloud_color)
    draw.ellipse([160, 200, 320, 340], fill='#BBDEFB')

    # 나무 줄기
    draw.rectangle([280, 310, 310, 400], fill='#8D6E63')

    # 나뭇잎
    draw.ellipse([230, 270, 360, 340], fill='#66BB6A')
    draw.ellipse([250, 250, 340, 310], fill='#81C784')

    # 태양
    sun_color = '#FFD54F'
    draw.ellipse([430, 60, 500, 130], fill=sun_color)

    # 텍스트 - 기본 폰트 사용
    try:
        # macOS 한글 폰트 시도
        font_large = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 48)
        font_small = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 28)
    except (IOError, OSError):
        try:
            font_large = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 48)
            font_small = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 28)
        except (IOError, OSError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # 메인 타이틀
    title = '하늘 꿈나무'
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 420), title, fill='#1565C0', font=font_large)

    # 서브 타이틀
    subtitle = '어린이집'
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((width - tw2) / 2, 490), subtitle, fill='#42A5F5', font=font_small)

    # 저장
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'static', 'images')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'og-logo.png')
    img.save(output_path, 'PNG', quality=95)
    print(f'OG 이미지 생성 완료: {output_path}')
    return output_path

if __name__ == '__main__':
    generate_og_image()
