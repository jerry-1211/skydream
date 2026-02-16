from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Faq


@admin_bp.route('/faqs/')
def faqs_list():
    faqs = Faq.query.order_by(Faq.sort_order, Faq.created_at.desc()).all()
    return render_template('admin/faqs/list.html', faqs=faqs)


@admin_bp.route('/faqs/create', methods=['GET', 'POST'])
def faqs_create():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not question or not answer:
            flash('질문과 답변을 모두 입력해주세요.', 'error')
            return render_template('admin/faqs/form.html', faq=None)

        faq = Faq(question=question, answer=answer, sort_order=sort_order, is_active=is_active)
        db.session.add(faq)
        db.session.commit()
        flash('FAQ가 등록되었습니다.', 'success')
        return redirect(url_for('admin.faqs_list'))

    return render_template('admin/faqs/form.html', faq=None)


@admin_bp.route('/faqs/<int:id>/edit', methods=['GET', 'POST'])
def faqs_edit(id):
    faq = Faq.query.get_or_404(id)

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not question or not answer:
            flash('질문과 답변을 모두 입력해주세요.', 'error')
            return render_template('admin/faqs/form.html', faq=faq)

        faq.question = question
        faq.answer = answer
        faq.sort_order = sort_order
        faq.is_active = is_active
        db.session.commit()
        flash('FAQ가 수정되었습니다.', 'success')
        return redirect(url_for('admin.faqs_list'))

    return render_template('admin/faqs/form.html', faq=faq)


@admin_bp.route('/faqs/<int:id>/delete', methods=['POST'])
def faqs_delete(id):
    faq = Faq.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.faqs_list'))
