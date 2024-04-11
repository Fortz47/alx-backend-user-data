#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns a formatted log record"""
        message = super().format(record)
        # message = re.sub(';', '; ', message)
        message = filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR
                              )
        return message.strip()
