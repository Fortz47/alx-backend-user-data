#!/usr/bin/env python3
"""Authentication Module"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if authentication is required"""
        try:
            path = path if path[-1] == '/' else path + '/'
            if path in excluded_paths:
                return False
            for _path in excluded_paths:
                if _path[-1] == '*':
                    _path = list(_path)
                    _path.pop()
                    pattern = ''.join(_path) + '.*?'
                    if re.search(pattern, path):
                        return False
        except Exception as e:
            print(e)
            pass
        return True

    def authorization_header(self, request=None) -> str:
        """returns authorization_header"""
        try:
            auth_header = request.headers.get('Authorization')
            return auth_header
        except Exception:
            pass
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user"""
        return None
