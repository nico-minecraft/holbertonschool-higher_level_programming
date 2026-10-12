#!/usr/bin/python3
"""Simple API built with Flask."""
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage: username -> user dictionary
users = {}


@app.route("/")
def home():
    """Return a welcome message."""
    return "Welcome to the Flask API!"


@app.route("/data")
def get_data():
    """Return the list of all usernames."""
    return jsonify(list(users.keys()))


@app.route("/status")
def status():
    """Return the API status."""
    return "OK"


@app.route("/users/<username>")
def get_user(username):
    """Return the full object of the given user, or 404 if not found."""
    user = users.get(username)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/add_user", methods=["POST"])
def add_user():
    """Add a new user from the JSON body of the request."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    users[username] = data
    return jsonify({"message": "User added", "user": data}), 201


if __name__ == "__main__":
    app.run()
