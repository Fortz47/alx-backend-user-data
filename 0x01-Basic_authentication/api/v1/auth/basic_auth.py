#!/usr/bin/env python3
"""Module to manage Basic Auth"""
from api.v1.auth.auth import Auth
import base64


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
            username, pwd = decoded_base64_authorization_header.split(':', 1)
            return username.strip(), pwd.strip()
        except Exception:
            pass
        return None, None
