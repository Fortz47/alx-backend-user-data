#!/usr/bin/env python3
"""Module for views using session Auth"""
from api.v1.views import app_views
from models.user import User
from flask import make_response, jsonify, request
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login with session based Auth"""
    login_email, login_pwd = (
            request.form.get('email'),
            request.form.get('password')
        )
    login_email = login_email.strip() if login_email else login_email
    login_pwd = login_pwd.strip() if login_pwd else login_pwd
    if not login_email or len(login_email) == 0:
        return { "error": "email missing" }, 400
    if not login_pwd or len(login_pwd) == 0:
        return { "error": "password missing" }, 400
    user = None
    try:
        assert User.count()
        userList = User.search({'email': login_email})
        assert len(userList)
        user = userList[0]
        if not user.is_valid_password(login_pwd):
            return { "error": "wrong password" }, 401
    except Exception as e:
        return { "error": "no user found for this email" }, 404

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    session_name = os.getenv('SESSION_NAME')
    resp.set_cookie(session_name, session_id)
    return resp
