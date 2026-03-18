from flask import Blueprint, request, jsonify
from services.session_service import create_session, validate_session, destroy_session
from database.db_config import get_user_by_email
from utils.hash_utils import verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    session_id = create_session(user["id"])

    return jsonify({"message": "Login successful", "session_id": session_id})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    data = request.json
    session_id = data.get("session_id")

    destroy_session(session_id)

    return jsonify({"message": "Logged out"})


@auth_bp.route("/session/validate", methods=["POST"])
def validate():
    data = request.json
    session_id = data.get("session_id")

    user_id = validate_session(session_id)

    if user_id:
        return jsonify({"message": "Session valid", "user_id": user_id})
    
    return jsonify({"message": "Session expired"}), 401