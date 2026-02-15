from . import admin_bp
from .upload_helper import handle_image_upload
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Popup
from datetime import datetime


@admin_bp.route('/popups/')
def popups_list():
    popups = Popup.query.order_by(Popup.sort_order).all()
    return render_template('admin/popups/list.html', popups=popups)


@admin_bp.route('/popups/create', methods=['GET', 'POST'])
def popups_create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        link_url = request.form.get('link_url', '').strip()
        link_target = request.form.get('link_target', '_self').strip()
        is_active = request.form.get('is_active') == 'on'
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        show_today_hide = request.form.get('show_today_hide') == 'on'
        position = request.form.get('position', 'center').strip()
        width = request.form.get('width', 480, type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/popups/form.html', popup=None)

        image_id = handle_image_upload('photo', category='popup', alt_text=title)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        popup = Popup(
            title=title,
            content=content,
            image_id=image_id,
            link_url=link_url,
            link_target=link_target,
            is_active=is_active,
            start_date=start_date,
            end_date=end_date,
            show_today_hide=show_today_hide,
            position=position,
            width=width,
            sort_order=sort_order,
        )
        db.session.add(popup)
        db.session.commit()
        flash('팝업이 등록되었습니다.', 'success')
        return redirect(url_for('admin.popups_list'))

    return render_template('admin/popups/form.html', popup=None)


@admin_bp.route('/popups/<int:id>/edit', methods=['GET', 'POST'])
def popups_edit(id):
    popup = Popup.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        link_url = request.form.get('link_url', '').strip()
        link_target = request.form.get('link_target', '_self').strip()
        is_active = request.form.get('is_active') == 'on'
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        show_today_hide = request.form.get('show_today_hide') == 'on'
        position = request.form.get('position', 'center').strip()
        width = request.form.get('width', 480, type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not title:
            flash('제목을 입력해주세요.', 'error')
            return render_template('admin/popups/form.html', popup=popup)

        new_image_id = handle_image_upload('photo', category='popup', alt_text=title)
        if new_image_id:
            popup.image_id = new_image_id

        popup.title = title
        popup.content = content
        popup.link_url = link_url
        popup.link_target = link_target
        popup.is_active = is_active
        popup.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        popup.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        popup.show_today_hide = show_today_hide
        popup.position = position
        popup.width = width
        popup.sort_order = sort_order
        db.session.commit()
        flash('팝업이 수정되었습니다.', 'success')
        return redirect(url_for('admin.popups_list'))

    return render_template('admin/popups/form.html', popup=popup)


@admin_bp.route('/popups/<int:id>/delete', methods=['POST'])
def popups_delete(id):
    popup = Popup.query.get_or_404(id)
    db.session.delete(popup)
    db.session.commit()
    flash('팝업이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.popups_list'))
