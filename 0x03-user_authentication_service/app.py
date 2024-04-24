#!/usr/bin/env python3
"""simple flask app"""
from flask import (
        Flask,
        jsonify,
        request,
        make_response,
        abort,
        redirect,
        url_for
    )
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root():
    """home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_user():
    """adds a user to db if not exists"""
    email, pwd = request.form.get('email'), request.form.get('password')
    email = email.strip() if email else None
    pwd = pwd.strip() if pwd else None
    try:
        AUTH.register_user(email, pwd)
        return jsonify(
                {"email": email, "message": "user created"}
            )
    except ValueError:
        return jsonify(
                {"message": "email already registered"}
            ), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login and create a session"""
    email, pwd = request.form.get('email'), request.form.get('password')
    email = email.strip() if email else None
    pwd = pwd.strip() if pwd else None

    if AUTH.valid_login(email, pwd):
        session_id = AUTH.create_session(email)
        resp = make_response({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)
        return resp

    # Unauthorized
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session based on session id passed in cookie"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('root'))  # GET '/'

    abort(403)


@app.route('/profile', strict_slashes=False)
def profile():
    """returns user profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})

    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """reset password"""
    email = request.form.get('email')
    email = email.strip() if email else None
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update password in db"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    # remove possible trailing and/or leading white space
    email = email.strip() if email else None
    reset_token = reset_token.strip() if reset_token else None
    new_password = new_password.strip() if new_password else None

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
