#!/usr/bin/env python3
"""Module to manage session expiration"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """manages session expiration"""
    def __init__(self):
        """initalize"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a user ID based on session ID"""
        try:
            assert session_id is not None
            assert self.user_id_by_session_id.get(session_id) is not None
            user_id = self.user_id_by_session_id.get(session_id)\
                .get('user_id')
            created_at = self.user_id_by_session_id.get(session_id)\
                .get('created_at')
            assert created_at is not None
            seconds_in_timedelta = timedelta(seconds=self.session_duration)
            assert created_at + seconds_in_timedelta > datetime.now()
            return user_id
        except Exception:
            pass
        return None
