from flask import Blueprint, request, jsonify
from .models import User
from bcrypt import checkpw
from movies_api.utils import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


users_bp = Blueprint("user", __name__)


@users_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    username = payload.get("username")
    if username is None:
        return {"error": "No username provided"}, 400
    password = payload.get("password")
    if password is None:
        return {"error": "No password provided"}, 400
    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        return {"error": "User not found"}, 404
    if not checkpw(password.encode(), user.password_hash.encode()):
        return {"error": "Invalid password"}, 403
    return jsonify(access_token=create_access_token(identity=username)), 200


@users_bp.route("/check")
@jwt_required()
def check():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello {current_user}"), 200
