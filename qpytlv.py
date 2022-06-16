#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :qpytlv.py
@author    :Chavis.Chen (chavis.chen@quectel.com)
@brief     :tlv parsing on Quecpython
@version   :0.1
@date      :2022-05-07 11:59:51
@copyright :Copyright (c) 2022
"""

from usr.TLV import TLV, ErrorNo

class QpyTLVError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class QpyTLV(object):
    def __init__(self, tags=None):
        self._tlv = TLV(tags)

    def parse(self, tlv_data):
        if type(tlv_data) is bytes or type(tlv_data) is bytearray:
            return self._tlv.parse(tlv_data)
        else:
            raise TypeError("tlv_data must be bytes or bytearray.")

    def get_parse_position(self):
        return self._tlv.get_parse_position()

    def _build(self, data, upper_data=None, upper_tag=None):
        """
        Argument format:
        {
            <tag0_str>: {
                <tag1_str>: {
                    <tag2_str1>: <value>,
                    <tag2_str2>: <value>
                }
            }
        }

        For example:
        {
            "0000": {
                "0100": {
                    "0200": b'\x00\x01\x02\x03'
                    "0201": {
                        "0300": b'\x00\x01\x02\x03'
                    }
                }
            }
        }
        """

        nested_key = []

        if type(data) is not dict:
            raise TypeError("data must be dict.")

        for key, value in data.items():
            if not (type(value) is bytes or type(value) is bytearray):
                nested_key.append(key)

        if len(nested_key):
            for key in nested_key:
                self._build(data[key], data, key)

        r_code, r_data = self._tlv.build(data)
        if r_code != ErrorNo.NO_ERROR:
            raise QpyTLVError("tlv build failed: %s" % r_code)

        if upper_data:
            upper_data[upper_tag] = r_data

        return r_data

    def build(self, data):
        return self._build(data)
