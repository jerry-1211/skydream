from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import SiteInfo, Media


@admin_bp.route('/site-info/', methods=['GET', 'POST'])
def site_info_edit():
    if request.method == 'POST':
        for key in SiteInfo.KEYS:
            if key == 'about_hero_image_id':
                continue  # handled separately below
            value = request.form.get(key, '').strip()
            SiteInfo.set_value(key, value)

        # Handle about hero image upload
        new_photo_id = handle_image_upload('about_hero_image', category='about', alt_text='어린이집 소개 대표 이미지')
        if new_photo_id:
            SiteInfo.set_value('about_hero_image_id', str(new_photo_id))

        db.session.commit()
        flash('사이트 정보가 저장되었습니다.', 'success')
        return redirect(url_for('admin.site_info_edit'))

    # Load all current values
    site_values = {}
    for key in SiteInfo.KEYS:
        site_values[key] = SiteInfo.get_value(key)

    # Load current hero image for preview
    hero_image = None
    hero_image_id = site_values.get('about_hero_image_id', '')
    if hero_image_id:
        hero_image = Media.query.get(int(hero_image_id))

    return render_template('admin/site_info/form.html', keys=SiteInfo.KEYS, values=site_values, hero_image=hero_image)
