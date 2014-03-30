# -*- coding: utf-8 -*-
"""
Email message objects.
"""
from __future__ import unicode_literals

import copy
import StringIO
from email.message import Message


class MessagePart(object):

    """
    Message part class. This is a base class for extending the UnicodeMessage
    and Attachment classes. Basically handles all of the header handling.
    """

    headers = None

    def set_all_headers(self, headers):
        """Copy specified headers to this class replacing any exsiting
        headers in the process.

        Args:
            headers (list): List of key, value pairs.
        """
        self.headers = copy.copy(headers or list())

    def set_header(self, name, value):
        """Set the value for a header. Headers are stored in the order
        they are first recieved. This method allows for setting multiple
        headers with the same name. Use `replace_header` if you wish to
        replace all other headers with this name with the one being added.

        Args:
            name (unicode): The name of the header.
            value (unicode): The value for the header.
        """
        if self.headers is None:
            self.headers = [(name, value)]
        else:
            self.headers.append((name, value))

    def delete_header(self, name):
        """Delete all occurrences of the header with the given name.

        Args:
            name (unicode): The name of the header.
        """
        if self.headers is not None:
            self.headers = [(key, value) for (key, value) in self.headers \
                    if key != name]

    def replace_header(self, name, value):
        """Replace the value for a header. Headers are stored in the order
        they are first recieved. This method will remove existing headers
        with the same name. Use `set_header` if you wish to set another
        header with by the same name.

        Args:
            name (unicode): The name of the header.
            value (unicide): The value of the header.
        """
        self.delete_header(name)
        self.set_header(name, value)


class Attachment(MessagePart):

    """
    Message attachment class. Contains the raw content for the attachment
    as well as a minimal set of headers as they pertain to the attachment's
    content. These headers should include stuff like type and disposition.
    """

    def __init__(self, content=None, headers=None):
        """Initialize instance of Attachment.

        Args:
            content (string): The content of the message attachment.
            headers (dict): Headers describing the message attachment.
        """
        self.set_all_headers(headers)
        self.content = content

    def as_dict(self):
        """Return the message attachment as a dictionary."""
        return {
            'headers': self.headers,
            'content': self.content,
        }

    def set_content(self, content):
        """Set the content to `content` if it's a file handle, else if it's
        a string, assume it's the content itself and wrap it in a StringIO.

        Args:
            content (string|object): content as a string or as file handle.
        """
        if hasattr(content, 'read'):
            self.content = content
        else:
            self.content = StringIO.StringIO(content)


class UnicodeMessage(MessagePart):

    """
    Message object headers and body are Unicode rather than RFC-2047
    encoded byte arrays. Attachments are separated from the message
    parts.
    """

    def __init__(self):
        """Initialize instance of UnicodeMessage."""
        self.headers = list()
        self.message_parts = list()
        self.attachments = list()

    def as_dict(self):
        """Return the message headers and body as a dictionary."""
        return {
            'headers': self.headers,
            'message_parts': self.message_parts,
            'attachments': [attachment.as_dict() \
                    for attachment in self.attachments],
        }

    def as_string(self):
        """Return the message headers and body flattened as a string."""
        return ''

    def __str__(self):
        """Equivalent to as_string()."""
        return self.as_string()

    def is_multipart(self):
        """Return whether or not this is a multipart message."""
        return self.attachments or len(self.message_parts) > 1

    def set_message_part(self, message_body, content_type='text/plain'):
        """Set a message part (The body of the message). Message parts are
        stored in the order they are received.

        Args:
            message_body (unicode): The contents of the body of this mesage
                part.
            content_type (unicode): The content type for this message part.
                Defaults to 'text/plain'.
        """
        self.message_parts.append((content_type, message_body))

    def enqueue_attachment(self, attachment):
        """Add an attachment to the end of the attachment queue.

        Args:
            attachment (Attachment): The attachment we are adding.
        """
        self.attachments.append(attachment)

    def dequeue_attachment(self):
        """Remove the first attachment from the front of the attachment queue.

        Returns:
            (Attachment) The attachment on the front of the queue.
        """
        self.attachments.popleft(attachment)

