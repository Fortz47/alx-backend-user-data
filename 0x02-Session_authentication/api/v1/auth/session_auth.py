#!/usr/bin/env python3
"""A module for managing session based authentication"""
from api.v1.auth.auth import Auth
import uuid


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
