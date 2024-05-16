#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in a log message.
It is designed to be used where log data needs redaction of sensitive information.
"""

import re

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specific fields in a log message.

    Args:
    fields (list): A list of strings representing the fields to obfuscate.
    redaction (str): The string to replace the contents of the fields with.
    message (str): The log message containing the fields.
    separator (str): The character that separates fields in the message.

    Returns:
    str: The message with specified fields obfuscated.
    """
    pattern = separator.join([f'(?<={field}=)[^;]+' for field in fields])
    return re.sub(pattern, redaction, message)

if __name__ == "__main__":
    # Test code that prints obfuscated messages.
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
    ]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
