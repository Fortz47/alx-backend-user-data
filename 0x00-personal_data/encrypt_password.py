#!/usr/bin/env python3
"""A module to hash paswords with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a hashed password"""
    # Hash a password for the first time, with a randomly-generated salt
    pwd = bytes(password, encoding='utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed
