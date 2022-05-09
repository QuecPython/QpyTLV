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

from usr.TLV import TLV, data2hexstring

class QpyTLV(object):
    def __init__(self, tags=None):
        self._tlv = TLV(tags)

    def parse(self, tlv_data):
        if type(tlv_data) is bytes or type(tlv_data) is bytearray:
            tlv_string = data2hexstring(tlv_data)
            return self._tlv.parse(tlv_string)
        else:
            raise TypeError("tlv_data must be bytes or bytearray.")
    
    def _build_low(self, data, upper_data=None):
        """
        Argument format:
        {
            <tag0_str>: {
                <tag1_str>: {
                    <tag2_str>: value
                }
            }
        }

        For example:
        {
            "0000": {
                "0100": {
                    "0200": b'\x00\x01\x02\x03'
                }
            }
        }
        """

        if type(data) is not dict:
            raise TypeError("data must be dict.")

        if(len(data) != 1):
            raise ValueError("len(data) must be 1.")

        value = list(data.items())[0][1]
        res = b''
        if type(value) is bytes or type(value) is bytearray:
            res = self._tlv.build(data)
            if upper_data:
                upper_tag = list(upper_data.items())[0][0]
                upper_data[upper_tag] = res
        else:
            res = self._build_low(value, data)
        return res

    def _build(self, data):
        if type(data) is not dict:
            raise TypeError("data must be dict.")

        while type(list(data.items())[0][1]) is dict:
            self._build_low(data)

        return self._build_low(data)

    def build(self, data):
        return self._build(data)
