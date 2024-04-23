#!/usr/bin/env python3
"""User table Module"""
from sqlalchemy import (
        Column,
        Integer,
        String,
    )
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """User clase table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
