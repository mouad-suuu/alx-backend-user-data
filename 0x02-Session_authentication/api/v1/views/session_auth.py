#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Handles user login and creates a new session.
    Return:
        - JSON representation of a User object.
    """
    not_found_res = {"error": "no user found for this email"}

    # Retrieve email and password from the request form
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    # Search for users with the provided email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404

    # Check if user is found and validate the password
    if len(users) <= 0:
        return jsonify(not_found_res), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        # Set the session ID in the cookie
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Handles user logout and destroys the current session.
    Return:
        - An empty JSON object.
    """
    from api.v1.app import auth

    # Attempt to destroy the session
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)

    return jsonify({})
