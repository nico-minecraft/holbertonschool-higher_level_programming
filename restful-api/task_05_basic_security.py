#!/usr/bin/python3
"""API security: Basic Auth, JWT authentication and role-based access."""
import os

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Use a strong secret from the environment in real deployments.
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "change-me-to-a-long-random-secret-key-0123456789"
)

auth = HTTPBasicAuth()
jwt = JWTManager(app)

users = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user",
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin",
    },
}


# ---------------------------------------------------------------------------
# Basic Authentication
# ---------------------------------------------------------------------------
@auth.verify_password
def verify_password(username, password):
    """Return the username if the credentials are valid, else None."""
    user = users.get(username)
    if user and check_password_hash(user["password"], password):
        return username
    return None


@auth.error_handler
def basic_auth_error(status):
    """Return 401 for any basic authentication failure."""
    return jsonify({"error": "Unauthorized"}), 401


@app.route("/basic-protected")
@auth.login_required
def basic_protected():
    """Route protected with Basic Auth."""
    return "Basic Auth: Access Granted"


# ---------------------------------------------------------------------------
# JWT Authentication
# ---------------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    """Validate credentials and return a JWT access token."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid credentials"}), 401

    username = data.get("username")
    password = data.get("password")
    user = users.get(username) if isinstance(username, str) else None

    if (user is None or not isinstance(password, str)
            or not check_password_hash(user["password"], password)):
        return jsonify({"error": "Invalid credentials"}), 401

    # The identity is the username; the role is embedded in the payload.
    token = create_access_token(
        identity=username,
        additional_claims={"role": user["role"]},
    )
    return jsonify({"access_token": token})


@app.route("/jwt-protected")
@jwt_required()
def jwt_protected():
    """Route protected with a JWT token."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Route restricted to users with the admin role."""
    if get_jwt().get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


# ---------------------------------------------------------------------------
# JWT error handlers: every authentication error must return 401
# ---------------------------------------------------------------------------
@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    """Missing token."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    """Malformed or badly signed token."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def handle_expired_token_error(jwt_header, jwt_data):
    """Expired token."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def handle_revoked_token_error(jwt_header, jwt_data):
    """Revoked token."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(jwt_header, jwt_data):
    """Fresh token required."""
    return jsonify({"error": "Fresh token required"}), 401


if __name__ == "__main__":
    app.run()
