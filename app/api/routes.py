from flask import jsonify, g
from app.models import Item, LogEntry
from app.decorators import require_api_key
from . import api_bp  # импорт из текущего пакета


@api_bp.route('/items', methods=['GET'])
@require_api_key
def get_items():
    user = g.api_user
    items = Item.query.filter_by(user_id=user.id).order_by(Item.created_at.desc()).all()
    return jsonify([{
        'id': it.id,
        'name': it.name,
        'description': it.description,
        'created_at': it.created_at.isoformat()
    } for it in items])


@api_bp.route('/logs', methods=['GET'])
@require_api_key
def get_logs():
    user = g.api_user
    logs = LogEntry.query.filter_by(user_id=user.id).order_by(LogEntry.timestamp.desc()).all()
    return jsonify([{
        'id': lg.id,
        'action': lg.action,
        'item_id': lg.item_id,
        'item_name': lg.item_name,
        'item_description': lg.item_description,
        'timestamp': lg.timestamp.isoformat()
    } for lg in logs])
