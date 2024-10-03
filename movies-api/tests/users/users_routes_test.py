from flask import Flask
import pytest
from movies_api.users.models import User
from movies_api.utils import jwt, db
from movies_api.users.routes import users_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test"
    jwt.init_app(app)
    app.register_blueprint(users_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add(User("test", "password"))
        db.session.commit()
        yield app.test_client()
        db.drop_all()


def test_login(client):
    response = client.post("/login", json={"username": "test", "password": "password"})
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["access_token"]


def test_login_wrong_password(client):
    response = client.post("/login", json={"username": "test", "password": "wrong"})
    assert response.status_code == 403


def test_login_no_user(client):
    response = client.post("/login", json={"password": "password"})
    assert response.status_code == 400


def test_login_user_not_found(client):
    response = client.post(
        "/login", json={"username": "not_found", "password": "password"}
    )
    assert response.status_code == 404


def test_login_no_password(client):
    response = client.post("/login", json={"username": "test"})
    assert response.status_code == 400


def test_check_no_token(client):
    response = client.get("/check")
    assert response.status_code == 401


@pytest.fixture
def access_token(client):
    response = client.post("/login", json={"username": "test", "password": "password"})
    response_json = response.get_json()
    return response_json["access_token"]


def test_check(client, access_token):
    response = client.get("/check", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["message"] == "Hello test"
