#!/usr/bin/env python3
"""A module for managing session based authentication"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """manages session based Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a user ID"""
        try:
            assert user_id is not None
            assert isinstance(user_id, str)
        except Exception:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user ID based on session ID"""
        try:
            assert session_id is not None
            assert isinstance(session_id, str)
        except Exception:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if self.user_id_by_session_id.get(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
