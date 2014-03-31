# -*- coding: utf-8 -*-
"""
Tests against message classes.
"""
from __future__ import unicode_literals

import unittest
from collections import deque

from email_cleanse.message import MessagePart, UnicodeMessage, Attachment


class TestMessagePart(unittest.TestCase):

    def test_set_all_headers(self):
        msg = MessagePart()
        headers = [('From', 'jim@example.com'), ('To', 'bob@example.com')]
        msg.set_all_headers(headers)
        # Order preserved.
        self.assertEqual([
                ('From', 'jim@example.com'),
                ('To', 'bob@example.com'),
            ], msg.headers)
        # Ensure mutablity of headers propery maintained.
        headers[0] = ('From', 'jon@example.com')
        self.assertEqual([
                ('From', 'jim@example.com'),
                ('To', 'bob@example.com'),
            ], msg.headers)

    def test_get_headers_as_string(self):
        msg = MessagePart()
        msg.add_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.add_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.add_header('To', '"Bob Smith" <bob@example.com>')
        msg.add_header('Subject', 'This is a test')
        msg.add_header('From', 'jim@example.com')
        # Order is preserved.
        self.assertEqual("Date: Wed, 24 Mar 2012 12:55:34 +0000\n" +
                "Message-Id: <201203241234dA120Pp@foo.bar>\n" +
                "To: \"Bob Smith\" <bob@example.com>\n" +
                "Subject: This is a test\n" +
                "From: jim@example.com\n",
                msg.get_headers_as_string())

    def test_set_header(self):
        msg = MessagePart()
        msg.add_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.add_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.add_header('To', '"Bob Smith" <bob@example.com>')
        msg.add_header('Subject', 'This is a test')
        msg.add_header('From', 'jim@example.com')
        # Order is preserved.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
            ], msg.headers)
        msg.add_header('Date', 'Tue, 23 Mar 2012 01:23:54 +0000')
        # Order remains unchanged. Second `Date` header added to
        # end of list.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
                ('Date', 'Tue, 23 Mar 2012 01:23:54 +0000'),
            ], msg.headers)

    def test_delete_header(self):
        msg = MessagePart()
        msg.add_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.add_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.add_header('To', '"Bob Smith" <bob@example.com>')
        msg.delete_header('Message-Id')
        # Message-Id header no longer included.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('To', '"Bob Smith" <bob@example.com>'),
            ], msg.headers)

    def test_delete_header_when_none(self):
        msg = MessagePart()
        msg.delete_header('Message-Id')
        self.assertEqual(None, msg.headers)

    def replace_header(self):
        msg = MessagePart()
        msg.add_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.add_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.add_header('To', '"Bob Smith" <bob@example.com>')
        msg.add_header('Subject', 'This is a test')
        msg.add_header('From', 'jim@example.com')
        # Order is preserved.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
            ], msg.headers)
        msg.replace_header('Date', 'Tue, 23 Mar 2012 01:23:54 +0000')
        # Order changed. Second `Date` replaces filrst and appended to
        # end of list.
        self.assertEqual([
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
                ('Date', 'Tue, 23 Mar 2012 01:23:54 +0000'),
            ], msg.headers)

    def replace_header_when_none(self):
        msg = MessagePart()
        msg.replace_header('Date', 'Tue, 23 Mar 2012 01:23:54 +0000')
        self.assertEqual([
                ('Date', 'Tue, 23 Mar 2012 01:23:54 +0000'),
            ], msg.headers)


class TestAttachment(unittest.TestCase):

    def test_add_header(self):
        """TODO: Test that we only set headers we want to keep."""
        pass

    def test_set_content(self):
        att = Attachment()
        att.set_content('This is my attachment')
        self.assertEqual('This is my attachment', att.content.read())

    def test_as_dict(self):
        att = Attachment()
        att.add_header('Content-Disposition', 'foo')
        att.set_content('This is my attachment')
        self.assertEqual({
                'content': 'This is my attachment',
                'headers': [('Content-Disposition', 'foo')],
            }, att.as_dict())


class TestUnicodeMessage(unittest.TestCase):

    def test_add_message_part(self):
        msg = UnicodeMessage()
        msg.add_message_part('This is the text part')
        msg.add_message_part(
                '<html><body><b>This is the HTML part</b></body></html>',
                'text/html')
        # Order is preserved. First part gets default 'text/plain'.
        self.assertEqual([
                ('text/plain', 'This is the text part'),
                ('text/html', '<html><body><b>This is the HTML part</b>' + \
                    '</body></html>'),
            ], msg.message_parts)

    def test_enqueue_attachment(self):
        msg = UnicodeMessage()
        att_a = Attachment()
        att_b = Attachment()
        msg.enqueue_attachment(att_a)
        self.assertEqual(deque([att_a]), msg.attachments)
        msg.enqueue_attachment(att_b)
        self.assertEqual(deque([att_a, att_b]), msg.attachments)

    def test_dequeue_attachment(self):
        msg = UnicodeMessage()
        att_a = Attachment()
        att_b = Attachment()
        msg.enqueue_attachment(att_a)
        msg.enqueue_attachment(att_b)
        self.assertEqual(deque([att_a, att_b]), msg.attachments)
        dequeued_att = msg.dequeue_attachment()
        self.assertEqual(att_a, dequeued_att)
        self.assertEqual(deque([att_b]), msg.attachments)

    def test_is_multipart_alternative_single_type(self):
        msg = UnicodeMessage()
        self.assertFalse(msg.is_multipart())
        msg.add_message_part('This is the text part')
        self.assertFalse(msg.is_multipart())
        msg.add_message_part('This is another text part')
        self.assertTrue(msg.is_multipart())

    def test_is_multiplart_alternative(self):
        msg = UnicodeMessage()
        msg.add_message_part('This is the text part')
        self.assertFalse(msg.is_multipart())
        msg.add_message_part('<b>This is HTML</b>', 'text/html')
        self.assertTrue(msg.is_multipart())

    def test_is_multipart_attachments(self):
        msg = UnicodeMessage()
        att_a = Attachment()
        msg.enqueue_attachment(att_a)
        self.assertTrue(msg.is_multipart())

    def test_as_dict(self):
        msg = UnicodeMessage()
        msg.add_header('To', '"Bob Smith" <bob@example.com>')
        msg.add_header('Subject', 'This is a test')
        att_a = Attachment()
        msg.enqueue_attachment(att_a)
        msg.add_message_part('This is the text part')
        self.assertEqual({
                'headers': [
                    ('To', '"Bob Smith" <bob@example.com>'),
                    ('Subject', 'This is a test')],
                'message_parts': [
                    ('text/plain', 'This is the text part')],
                'attachments': [
                    {'content': '', 'headers': []}]
            }, msg.as_dict())

