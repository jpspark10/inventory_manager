from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort, jsonify, g, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, Item, LogEntry
from .forms import RegistrationForm, LoginForm, ItemForm
from . import auth_bp
from app.decorators import require_api_key


api_bp = Blueprint('api', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web.list_items'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        # Создаем новый предмет с названием и описанием
        item = Item(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()

        # Добавляем запись в логи
        log_entry = LogEntry(
            action=f"Удалён предмет: {item.name}",
            item_id=item.id,
            item_name=item.name,
            item_description=item.description,
            timestamp=datetime.utcnow(),
            user_id=current_user.id
        )
        db.session.add(log_entry)
        db.session.commit()

        flash('Предмет успешно добавлен!', 'success')
        return redirect(url_for('auth.items'))
    return render_template('add_item.html', form=form)


@auth_bp.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        abort(403)

    form = ItemForm(obj=item)
    if form.validate_on_submit():
        old_name = item.name
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()

        log_entry = LogEntry(
            action=f"Изменён предмет: {old_name} → {item.name}",
            item_id=item.id,
            timestamp=datetime.utcnow(),
            user_id=current_user.id
        )
        db.session.add(log_entry)
        db.session.commit()

        flash('Предмет обновлен!', 'success')
        return redirect(url_for('auth.items'))

    return render_template('edit_item.html', form=form, item=item)


@auth_bp.route('/items/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        abort(403)

    db.session.delete(item)

    log_entry = LogEntry(
        action=f"Удалён предмет: {item.name}",
        item_id=item.id,
        timestamp=datetime.utcnow(),
        user_id=current_user.id
    )
    db.session.add(log_entry)
    db.session.commit()

    flash('Предмет удален!', 'success')
    return redirect(url_for('auth.items'))


@auth_bp.route('/api_key', methods=['GET', 'POST'])
@login_required
def api_key():
    if current_user.api_key_valid():
        api_key = current_user.api_key
        expiration = current_user.api_key_expiration
    else:
        api_key = None
        expiration = None

    if 'generate' in request.args:
        current_user.generate_api_key()
        flash('Новый API ключ сгенерирован и действителен 30 дней.', 'success')
        return redirect(url_for('auth.api_key'))

    return render_template('api_key.html', api_key=api_key, expiration=expiration)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.items'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('auth.items'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/items')
@login_required
def items():
    # Передаем список предметов в шаблон
    items = Item.query.all()
    return render_template('items.html', items=items)


@auth_bp.route('/logs')
@login_required
def logs():
    logs = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)

