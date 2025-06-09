import pytest
from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'LOGIN_DISABLED': False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def new_user():
    user = User(username='testuser')
    user.set_password('testpass')
    return user


@pytest.fixture
def logged_in_client(client, app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    return client
