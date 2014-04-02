# -*- coding: utf-8 -*-
"""
Email message objects.
"""
from __future__ import unicode_literals

import copy
import StringIO
from collections import deque
from email.message import Message


class MessagePart(object):

    """
    Message part class. This is a base class for extending the UnicodeMessage
    and Attachment classes. Basically handles all of the header handling.
    """

    def __init__(self, headers=None):
        """Initialize instance of MessagePart.

        Args:
            headers (dict): Headers describing the message part.
        """
        if headers is None:
            self.headers = list()
        else:
            self.set_all_headers(headers)

    def set_all_headers(self, headers):
        """Copy specified headers to this class replacing any exsiting
        headers in the process.

        Args:
            headers (list): List of key, value pairs.
        """
        self.headers = copy.copy(headers or list())

    def get_headers_as_string(self):
        """Get headers as a string. Each header on it's own line in order as
        name-colon-space-value. Last header also ends with a new-line. Example::

            Date: Wed, 24 Mar 2012 12:55:34 +0000\n
            Message-Id: <201203241234dA120Pp@foo.bar>\n
            To: "Bob Smith" <bob@example.com>\n
            Subject: This is a test\n
            From: jim@example.com\n
        """
        return ''.join("{0}: {1}\n".format(name, value) for name, value in \
                self.headers)

    def add_header(self, name, value):
        """Add the name, value pair for a header. Headers are stored in the
        order they are first recieved. This method allows for setting multiple
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
        self.add_header(name, value)


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
        super(Attachment, self).__init__(headers)
        self.content = content

    def as_dict(self):
        """Return the message attachment as a dictionary."""
        if self.content:
            self.content.seek(0)
            return {
                'headers': self.headers,
                'content': self.content.read(),
            }
        else:
            return {
                'headers': self.headers,
                'content': '',
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
        super(UnicodeMessage, self).__init__()
        self.alternatives = list()
        self.attachments = deque()
        self.message_parts = list()

    def as_dict(self):
        """Return the message headers and body as a dictionary."""
        return {
            'headers': self.headers,
            'alternatives': self.alternatives,
            'attachments': [attachment.as_dict() \
                    for attachment in self.attachments],
        }

    def is_multipart(self):
        """Return whether or not this is a multipart message."""
        return self.attachments or len(self.alternatives) > 1 \
                or self.message_parts

    def add_alternative(self, message_body, content_type='text/plain'):
        """Add a message alternative (The body of the message). Alternatives are
        stored in the order they are received.

        Args:
            message_body (unicode): The contents of the body of this message
                alternative.
            content_type (unicode): The content type for this alternative.
                Defaults to 'text/plain'.
        """
        self.alternatives.append((content_type, message_body))

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
        return self.attachments.popleft()

