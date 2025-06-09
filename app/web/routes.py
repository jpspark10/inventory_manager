from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Item, LogEntry
from . import web_bp
from .forms import ItemForm


@web_bp.route('/', methods=['GET'])
@login_required
def list_items():
    """
    Главная страница — список предметов.
    """
    items = Item.query.filter_by(user_id=current_user.id).all()
    form = ItemForm()
    return render_template('items.html', items=items, form=form)


@web_bp.route('/add', methods=['POST'])
@login_required
def add_item():
    """
    Обработка формы добавления предмета.
    """
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(item)
        db.session.flush()
        log = LogEntry(action='add', item_name=item.name, user_id=current_user.id)
        db.session.add(log)
        db.session.commit()
        flash('Предмет добавлен.', 'success')
    else:
        flash('Ошибка при добавлении. Проверьте форму.', 'danger')
    return redirect(url_for('web.list_items'))


@web_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    """
    Удаление предмета и логирование.
    """
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Нет прав для удаления этого предмета.', 'danger')
    else:
        db.session.delete(item)
        log = LogEntry(action='delete', item_name=item.name, user_id=current_user.id)
        db.session.add(log)
        db.session.commit()
        flash('Предмет удалён.', 'info')
    return redirect(url_for('web.list_items'))
