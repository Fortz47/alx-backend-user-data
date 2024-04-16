#!/usr/bin/env python3
"""Module to manage Basic Auth"""
from api.v1.auth.auth import Auth


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
