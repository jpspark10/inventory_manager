from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models import User, Item, LogEntry

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """Создаёт все таблицы."""
    db.create_all()
    print("База данных создана.")


@cli.command("drop_db")
def drop_db():
    """Удаляет все таблицы."""
    db.drop_all()
    print("База данных удалена.")


@cli.command("seed_db")
def seed_db():
    """Создаёт тестового пользователя и несколько предметов."""
    user = User(username="admin")
    user.set_password("adminpass")
    db.session.add(user)
    db.session.flush()

    for i in range(3):
        item = Item(
            name=f"Item {i + 1}",
            description=f"Sample item {i + 1}",
            user_id=user.id
        )
        db.session.add(item)

    db.session.commit()
    print("Данные успешно добавлены.")


if __name__ == "__main__":
    cli()
