import json
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import MealPlan
from datetime import date


@admin_bp.route('/meals/')
def meals_list():
    page = request.args.get('page', 1, type=int)
    pagination = MealPlan.query.order_by(
        MealPlan.plan_date.desc(), MealPlan.meal_type
    ).paginate(page=page, per_page=10)
    return render_template('admin/meals/list.html', pagination=pagination)


@admin_bp.route('/meals/create', methods=['GET', 'POST'])
def meals_create():
    if request.method == 'POST':
        plan_date_str = request.form.get('plan_date', '').strip()
        meal_type = request.form.get('meal_type', '').strip()
        menu_items_str = request.form.get('menu_items', '').strip()

        if not plan_date_str or not meal_type:
            flash('날짜와 식사 유형을 입력해주세요.', 'error')
            return render_template('admin/meals/form.html', meal=None, meal_types=MealPlan.MEAL_TYPES)

        try:
            plan_date = date.fromisoformat(plan_date_str)
        except ValueError:
            flash('올바른 날짜 형식이 아닙니다.', 'error')
            return render_template('admin/meals/form.html', meal=None, meal_types=MealPlan.MEAL_TYPES)

        # Parse menu items: one per line
        menu_items = [item.strip() for item in menu_items_str.split('\n') if item.strip()]

        meal = MealPlan(
            plan_date=plan_date,
            meal_type=meal_type,
        )
        meal.menu_items = menu_items
        db.session.add(meal)
        db.session.commit()
        flash('급식 정보가 등록되었습니다.', 'success')
        return redirect(url_for('admin.meals_list'))

    return render_template('admin/meals/form.html', meal=None, meal_types=MealPlan.MEAL_TYPES)


@admin_bp.route('/meals/<int:id>/edit', methods=['GET', 'POST'])
def meals_edit(id):
    meal = MealPlan.query.get_or_404(id)

    if request.method == 'POST':
        plan_date_str = request.form.get('plan_date', '').strip()
        meal_type = request.form.get('meal_type', '').strip()
        menu_items_str = request.form.get('menu_items', '').strip()

        if not plan_date_str or not meal_type:
            flash('날짜와 식사 유형을 입력해주세요.', 'error')
            return render_template('admin/meals/form.html', meal=meal, meal_types=MealPlan.MEAL_TYPES)

        try:
            plan_date = date.fromisoformat(plan_date_str)
        except ValueError:
            flash('올바른 날짜 형식이 아닙니다.', 'error')
            return render_template('admin/meals/form.html', meal=meal, meal_types=MealPlan.MEAL_TYPES)

        menu_items = [item.strip() for item in menu_items_str.split('\n') if item.strip()]

        meal.plan_date = plan_date
        meal.meal_type = meal_type
        meal.menu_items = menu_items
        db.session.commit()
        flash('급식 정보가 수정되었습니다.', 'success')
        return redirect(url_for('admin.meals_list'))

    return render_template('admin/meals/form.html', meal=meal, meal_types=MealPlan.MEAL_TYPES)


@admin_bp.route('/meals/<int:id>/delete', methods=['POST'])
def meals_delete(id):
    meal = MealPlan.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    flash('급식 정보가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.meals_list'))
