#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Optional, Dict
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds user to db"""
        new_user = User(email=email, hashed_password=hashed_password)
        # new_user.email = email
        # new_user.hashed_password = hashed_pwd
        self._session
        self.__session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """finds a user based on passed attributes as arguments"""
        user_columns = [column.name for column in User.__table__.columns]
        if any(k not in user_columns for k in kwargs):
            raise InvalidRequestError
        if self.__session is None:
            self._session
        user = self.__session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
