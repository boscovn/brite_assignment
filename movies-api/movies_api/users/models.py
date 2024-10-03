from movies_api.utils import db
from bcrypt import gensalt, hashpw


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = hashpw(password.encode(), gensalt()).decode()
