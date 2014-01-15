# -*- coding: utf-8 -*-
"""
Email encoding.
"""
from __future__ import unicode_literals

import re
import chardet
from email.header import decode_header

JOIN_CHAR = "".encode('utf-8')

def get_decoded_email_header(text):
    """Get the decoded value for the email header text passed in.

    Args:
        text (string): RFC-2047 encoded header text.

    Returns:
        (unicode) The UTF-8 unicode representation for the header.
    """
    # Some email generation code creates invalid RFC-2047 headers
    # which do not include the required white-space separator. Attempt
    # to fix these using a simple regex substitution.
    text = re.sub(r"(=\?.*\?[BbQq]\?.*\?=)(?!$)", r"\1 ", text)
    parts = decode_header(text)
    decoded_parts = []
    for part, charset in parts:
        decoded_parts.append(decode_string_to_unicode(part, charset))
    return JOIN_CHAR.join(decoded_parts)

def decode_string_to_unicode(text, charset=None):
    """Get the unicode value of text using provided charset. If the charset
    is invalid attempt to guess what it is.

    Args:
        text (string): The string we want to decode.
        charset (string): The charset we think this is. Defaults to ascii.

    Returns:
        (unicode) The decoded unicode value.
    """
    try:
        if isinstance(text, unicode):
            return text
        return text.decode(charset or 'ascii', 'strict')
    except (UnicodeError, LookupError):
        charset = chardet.detect(text)
        return text.decode(charset['encoding'], 'replace')
