from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import SiteInfo


@admin_bp.route('/site-info/', methods=['GET', 'POST'])
def site_info_edit():
    if request.method == 'POST':
        for key in SiteInfo.KEYS:
            value = request.form.get(key, '').strip()
            SiteInfo.set_value(key, value)
        db.session.commit()
        flash('사이트 정보가 저장되었습니다.', 'success')
        return redirect(url_for('admin.site_info_edit'))

    # Load all current values
    site_values = {}
    for key in SiteInfo.KEYS:
        site_values[key] = SiteInfo.get_value(key)

    return render_template('admin/site_info/form.html', keys=SiteInfo.KEYS, values=site_values)
