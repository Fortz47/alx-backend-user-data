#!/usr/bin/env python3
"""simple flask app"""
from flask import Flask, jsonify, request
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
