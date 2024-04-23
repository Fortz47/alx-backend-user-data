#!/usr/bin/env python3
"""Module to handle security"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
