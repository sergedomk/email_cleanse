# -*- coding: utf-8 -*-
"""
Tests against utility functions.
"""
from __future__ import unicode_literals

import unittest

import email_utils.encoding

class TestEncoding(unittest.TestCase):
    def test_get_decoded_header(self):
        test_headers = [
            "=?iso-2022-jp?b?GyRCRW1CQE86GyhCIDxtb21vQHRhcm8ubmUuanA=?=",
            "honyaku@googlegroups.com",
            "\"=?UTF-8?Q?Igor_=C5=A0erko?=\"",
            "=?UTF-8?B?5qGD5aSqLCDpg44=?= ",
        ]
        for header in test_headers:
            decoded = email_utils.encoding.get_decoded_header(header)
            print decoded

    def test_get_decoded_header_subject(self):
        """
        Test material grabbed from questions regarding decoding email subject
        headers that I found on forums and blogs such as stackoverflow.
        """
        test_subjects = [
            "[ 201105161048 ] GewSt:=?UTF-8?B?IFdlZ2ZhbGwgZGVyIFZvcmzDpHV" + \
                "maWdrZWl0?=",
            "[ 201105191633 ] =?UTF-8?B?IERyZWltb25hdHNmcmlzdCBmw7xyIFZlc" + \
                "nBmbGVndW5nc21laHJhdWZ3ZW5kdW4=?= =?UTF-8?B?Z2VuIGVpbmVz" + \
                "IFNlZW1hbm5z?=",
            "'=?KOI8-R?B?W1JFUS0wMDI1NDEtNDc5NzddIO/h7yAi89TSz8rGwdLGz9Ii" + \
                "IDs=?=\r\n\t=?KOI8-R?B?Ry43MjkgKDEwKQ==?=",
            "[ 201101251025 ] ELStAM;=?UTF-8?B?IFZlcmbDvGd1bmcgdm9tIDIx?=" + \
                ". Januar 2011",
            "=?koi8-r?B?4tnT1NLP19nQz8zOyc3PIMkgzcHMz9rB1NLB1M7P?=",
            "=?ISO-8859-2?Q?=E9rdekes?=",
            "\"=?iso-2022-jp?b?GyRCS1xGfCRPQDJFNyRKJGobKEI=?=\"",
            "=?windows-1252?Q?Earn_your_degree_=97_on_your_time?=\n=?wind" + \
                "ows-1252?Q?_and_terms?=",
        ]
        for subject in test_subjects:
            decoded = email_utils.encoding.get_decoded_header(subject)
            print decoded


