#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        regx, repl = fr"{field}=.*?{sep}", fr"{field}={redaction}{sep}"
        msg = re.sub(regx, repl, msg)
    return msg
