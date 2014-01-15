# -*- coding: utf-8 -*-
"""
Tests against utility functions.
"""
from __future__ import unicode_literals

import unittest

import email_utils.encoding

class TestEncoding(unittest.TestCase):
    def test_get_decoded_email_header(self):
        test_headers = {
            "桃太郎 <momo@taro.ne.jp":
                "=?iso-2022-jp?b?GyRCRW1CQE86GyhCIDxtb21vQHRhcm8ubmUuanA=?=",
            "honyaku@googlegroups.com":
                "honyaku@googlegroups.com",
            "\"Igor Šerko\"": "\"=?UTF-8?Q?Igor_=C5=A0erko?=\"",
            "桃太, 郎": "=?UTF-8?B?5qGD5aSqLCDpg44=?= ",
            "桃太郎 <momo@taro.ne.jp>":
                "=?iso-2022-jp?b?GyRCRW1CQE86GyhCID?=\t<momo@taro.ne.jp>"
        }
        for header, encoded in test_headers.iteritems():
            decoded = email_utils.encoding.get_decoded_email_header(encoded)
            self.assertEqual(header, decoded)

    def test_get_decoded_email_header_subject(self):
        """
        Test material grabbed from questions regarding decoding email subject
        headers that I found on forums and blogs such as stackoverflow.
        """
        test_subjects = {
            "[ 201105161048 ] GewSt: Wegfall der Vorläufigkeit":
                "[ 201105161048 ] GewSt:=?UTF-8?B?IFdlZ2ZhbGwgZGVyIFZ" + \
                "vcmzDpHVmaWdrZWl0?=",
            "[ 201105191633 ] Dreimonatsfrist für Verpflegungsmehrauf" + \
            "wendungen eines Seemanns":
                "[ 201105191633 ] =?UTF-8?B?IERyZWltb25hdHNmcmlzdCBmw" + \
                "7xyIFZlcnBmbGVndW5nc21laHJhdWZ3ZW5kdW4=?= =?UTF-8?B?" + \
                "Z2VuIGVpbmVzIFNlZW1hbm5z?=",
            "[REQ-002541-47977] ОАО \"Стройфарфор\" ;G.729 (10)":
                "=?KOI8-R?B?W1JFUS0wMDI1NDEtNDc5NzddIO/h7yAi89TSz8rGw" + \
                "dLGz9IiIDs=?=\r\n\t=?KOI8-R?B?Ry43MjkgKDEwKQ==?=",
            "[ 201101251025 ] ELStAM; Verfügung vom 21. Januar 2011":
                "[ 201101251025 ] ELStAM;=?UTF-8?B?IFZlcmbDvGd1bmcgdm" + \
                "9tIDIx?=. Januar 2011",
            "Быстровыполнимо и малозатратно":
                "=?koi8-r?B?4tnT1NLP19nQz8zOyc3PIMkgzcHMz9rB1NLB1M7P?=",
            "érdekes":
                "=?ISO-8859-2?Q?=E9rdekes?=",
            "\"本日は晴天なり\"":
                "\"=?iso-2022-jp?b?GyRCS1xGfCRPQDJFNyRKJGobKEI=?=\"",
            "Earn your degree — on your time and terms":
                "=?windows-1252?Q?Earn_your_degree_=97_on_your_time?=" + \
                "\n=?windows-1252?Q?_and_terms?=",
            "pöstal":
                "=?foobar?q?p=F6stal?=",
        }
        for subject, encoded in test_subjects.iteritems():
            decoded = email_utils.encoding.get_decoded_email_header(encoded)
            self.assertEqual(subject, decoded)


