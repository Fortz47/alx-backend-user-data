#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re
from typing import List
import logging
import mysql.connector
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        return message


def get_logger() -> logging.Logger:
    """returns a logging.logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a mysql database connector object"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connection.MySQLConnection(
        user=user, password=pwd, host=host, database=db_name
    )


def main() -> None:
    """returns all row from db"""
    db = get_db()
    cursor = db.cursor()
    logger = get_logger()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        record = logging.LogRecord(None, None, None, None, row, None, None)
        print(logger.format(record))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
