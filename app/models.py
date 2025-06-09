from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    items = db.relationship('Item', backref='owner', lazy=True)
    logs = db.relationship('LogEntry', backref='user', lazy=True)
    api_key = db.Column(db.String(64), unique=True, nullable=True)
    api_key_expiration = db.Column(db.DateTime, nullable=True)

    def generate_api_key(self):
        import secrets
        self.api_key = secrets.token_hex(32)
        self.api_key_expiration = datetime.utcnow() + timedelta(days=30)
        db.session.commit()

    def api_key_valid(self):
        return self.api_key and self.api_key_expiration and datetime.utcnow() < self.api_key_expiration

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username!r}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.name!r}>'


class LogEntry(db.Model):
    __tablename__ = 'log_entry'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)  # теперь nullable
    item_name = db.Column(db.String(255), nullable=True)
    item_description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    item = db.relationship('Item')


