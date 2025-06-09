from flask import Blueprint

# Объявляем blueprint для веб‑части
web_bp = Blueprint(
    'web',
    __name__,
    template_folder='templates',   # Flask будет искать шаблоны в app/templates/
    static_folder='static'         # статические файлы (css, js) в app/static/
)

# Импортируем маршруты, чтобы они «прицепились» к web_bp
from . import routes  # noqa
