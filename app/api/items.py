from datetime import datetime

from flask import request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Item, LogEntry
from .blueprint import api_bp


@api_bp.route('/items/', methods=['GET'])
@login_required
def get_items():
    """
    Возвращает JSON со списком предметов текущего пользователя.
    """
    items = Item.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'created_at': item.created_at.isoformat()
        }
        for item in items
    ]), 200


@api_bp.route('/items/', methods=['POST'])
@login_required
def add_item():
    """
    Принимает JSON: { 'name': str, 'description': str (optional) }
    Создаёт новый предмет, логирует действие и возвращает его ID.
    """
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    description = data.get('description', '')

    item = Item(
        name=name,
        description=description,
        user_id=current_user.id
    )
    db.session.add(item)
    db.session.flush()  # чтобы item.id стал доступен

    log = LogEntry(
        action=f"Добавлен предмет: {item.name}",
        item_id=item.id,  # сюда передаем id предмета
        timestamp=datetime.utcnow(),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'id': item.id}), 201


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    """
    Удаляет предмет по ID, если он принадлежит текущему пользователю.
    Логирует действие. Возвращает 204 No Content.
    """
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(item)

    log = LogEntry(
        action='delete',
        item_name=item.name,
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()

    return '', 204


@api_bp.route('/logs/', methods=['GET'])
@login_required
def get_logs():
    """
    Возвращает JSON с журналом действий текущего пользователя:
    [{ 'action': 'add'|'delete', 'item_name': str, 'timestamp': ISO8601 }, ...]
    """
    logs = (
        LogEntry.query
        .filter_by(user_id=current_user.id)
        .order_by(LogEntry.timestamp.desc())
        .all()
    )
    return jsonify([
        {
            'action': log.action,
            'item_name': log.item_name,
            'timestamp': log.timestamp.isoformat()
        }
        for log in logs
    ]), 200
