#!/usr/bin/env python3
"""Module to manage Basic Auth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar
from flask import request


class BasicAuth(Auth):
    """manage Basic Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str
                                           ) -> str:
        """extrats base64 encoding"""
        try:
            auth_type, value = authorization_header.split(' ', 1)
            assert auth_type == 'Basic'
            return value.strip()
        except Exception:
            pass
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
                                          ) -> str:
        """returns the decoded value of a Base64 string"""
        try:
            res = base64.b64decode(base64_authorization_header)
            return res.decode('utf-8')
        except Exception:
            pass
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
                                ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value"""
        try:
            user_email, pwd = decoded_base64_authorization_header.split(':', 1)
            return user_email.strip(), pwd.strip()
        except Exception:
            pass
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
                                    ) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        try:
            assert not (user_email is None or user_pwd is None)
            assert isinstance(user_email, str) and isinstance(user_pwd, str)
            assert User.count()
            userList = User.search({'email': user_email})
            assert len(userList)
            user = userList[0]
            assert user.is_valid_password(user_pwd)
            return user
        except Exception as e:
            pass
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        try:
            auth_header = self.authorization_header(request=request)
            encoded_credentials = self.extract_base64_authorization_header(
                    auth_header
                )
            decoded_credentials = self.decode_base64_authorization_header(
                    encoded_credentials
                )
            user_email, user_pwd = self.extract_user_credentials(
                    decoded_credentials
                )
            user = self.user_object_from_credentials(user_email, user_pwd)
            return user
        except Exception:
            pass
        return None
