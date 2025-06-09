from functools import wraps
from flask import request, jsonify, g
from app.models import User


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        user = User.query.filter_by(api_key=api_key).first()
        if not user or not user.api_key_valid():
            return jsonify({'error': 'Invalid or expired API key'}), 403

        # сохраним пользователя в контекст запроса
        g.api_user = user
        return f(*args, **kwargs)
    return decorated_function
