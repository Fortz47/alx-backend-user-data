#!/usr/bin/env python3
"""A module to manage user session Model"""
from models.base import Base


class UserSession(Base):
    """user session Model"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
