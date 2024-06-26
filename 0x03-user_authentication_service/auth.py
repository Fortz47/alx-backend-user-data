#!/usr/bin/env python3
"""Module to handle security"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return random uuid"""
    return str(uuid.uuid4())


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
            user = self._db.add_user(email, hash_pwd)
            return user

        # user exists
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """check if login details is valid"""
        try:
            user = self._db.find_user_by(email=email)
            pwd = password.encode('utf-8')  # converts to bytes
            assert bcrypt.checkpw(pwd, user.hashed_password)
            return True
        except (NoResultFound, AssertionError):
            return False

    def create_session(self, email: str) -> str:
        """creates a session and return its id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """returns user based on session id or None"""
        try:
            assert session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, AssertionError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """sets the value of session id in db to None"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """update the user’s reset_token database field. Return the token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            pass

        raise ValueError

    def update_password(self, reset_token: str, password: str):
        """updates user password in db"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_pwd = _hash_password(password)
            kwargs = {'hashed_password': hash_pwd, 'reset_token': None}
            self._db.update_user(user.id, **kwargs)
            return None
        except NoResultFound:
            pass

        raise ValueError
