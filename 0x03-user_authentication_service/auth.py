#!/usr/bin/env python3
"""Module to handle security"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """adds a new user to db if not exists"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hash_pwd = _hash_password(password)
            self._db.add_user(email, hash_pwd)
            return self._db.find_user_by(email=email)

        # user exists
        raise ValueError(f'User {email} already exists')
