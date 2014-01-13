# -*- coding: utf-8 -*-
"""
Email encoding.
"""
from __future__ import unicode_literals

import re
from email.header import decode_header

JOIN_CHAR = "".encode('utf-8')

def get_decoded_header(text):
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
        part_decoded = part.decode(charset or 'ascii')
        decoded_parts.append(part_decoded.encode('utf-8'))
    return JOIN_CHAR.join(decoded_parts)


