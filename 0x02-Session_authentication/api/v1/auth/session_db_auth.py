#!/usr/bin/env python3
"""Session DB Auth Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """manage session instance in file DB"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
        and returns the Session ID"""
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
        in the database based on session_id"""
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions):
            user_session = user_sessions[0]
            created_at = user_session.created_at
            seconds_in_timedelta = timedelta(seconds=self.session_duration)
            if created_at + seconds_in_timedelta > datetime.now():
                return user_session.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """destroys the UserSession based on the Session
        ID from the request cookie"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 1:
            user_sessions[0].remove()
            return True
        return False
