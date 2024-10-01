from movies_api.users.models import User, db
from flask import Flask
import pytest
from bcrypt import checkpw


@pytest.fixture
def setup():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield
        db.drop_all()


def test_user(setup):
    user = User("test", "password")
    assert user.username == "test"
    assert user.password_hash != "password"
    assert checkpw("password".encode(), user.password_hash.encode())
    assert len(User.query.all()) == 0
    db.session.add(user)
    db.session.commit()
    users = User.query.all()
    assert len(users) == 1
    assert users[0].username == "test"
    assert checkpw("password".encode(), users[0].password_hash.encode())
    db.session.delete(user)
    db.session.commit()
    assert len(User.query.all()) == 0
