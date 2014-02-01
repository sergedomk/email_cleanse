
# -*- coding: utf-8 -*-
"""
Email message objects.
"""
from __future__ import unicode_literals

from email.message import Message
from collections import OrderedDict

class Attachment(object):
    pass


class UnicodeMessage(object):

    """
    Message object headers and body are Unicode rather than RFC-2047
    encoded byte arrays. Attachments are separated from the message
    parts.
    """

    headers = None
    message_parts = None
    attachments = None

    def __init__(self):
        """Initialize instance of UnicodeMessage."""
        self.headers = OrderedDict()
        self.message_parts = OrderedDict()
        self.attachments = set()

    def as_dict(self):
        """Return the message headers and body as a dictionary."""
        return {
            'headers': [(key, value) \
                    for key, value in self.headers.iteritems()],
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

    def set_header(self, name, value):
        """Set the value for a header. Headers are stored in the order
        they are first recieved. Setting the same header again does not
        effect the order.

        Args:
            name (unicode): The name of the header.
            value (unicode): The value for the header.
        """
        self.headers[name] = value

    def set_message_part(self, message_body, content_type='text/plain'):
        """Set a message part (The body of the message). Message parts are
        stored in the order they are received.

        Args:
            message_body (unicode): The contents of the body of this mesage
                part.
            content_type (unicode): The content type for this message part.
                Defaults to 'text/plain'.
        """
        self.message_parts[content_type] = message_body

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


class DigestMessage(object):
    pass


