#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
    ) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        regx, repl = (
            fr"{field}=.*?{separator}",
            fr"{field}={redaction}{separator}"
        )
        message = re.sub(regx, repl, message)
    return message
