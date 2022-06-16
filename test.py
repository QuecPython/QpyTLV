#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :test.py
@author    :Chavis.Chen (chavis.chen@quectel.com)
@brief     :test for qpytlv-iostream
@version   :0.1
@date      :2022-06-15 17:01:42
@copyright :Copyright (c) 2022
"""

from usr.qpytlv_iostream import QpyTLVIOAbs, QpyTLVIoStream
from usr.qpytlv import QpyTLV
from usr.serial import Serial
from machine import UART

class QpyTLVIO(QpyTLVIOAbs):
    def __init__(self):
        self._serial = Serial(UART.UART1)

    def read(self, timeout = 0):
        return self._serial.read(1024, timeout)

    def write(self, data):
        return self._serial.write(data)

def tlv_parse_cb(errno, parsed_data):
    print(errno, ",", parsed_data)


tags = ['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff', 'a5a5', 'e1e1']
qpytlv = QpyTLV(tags)
qpytlv_io = QpyTLVIO()
qpytlv_iostream = QpyTLVIoStream(qpytlv, qpytlv_io, tlv_parse_cb)

d = {
    "aaaa": b'\xaa\xaa',
    "bbbb": {
        "cccc": b'\xcc\xcc',
        "dddd": b'\xdd\xdd'
    },
    "eeee": {
        "ffff": b'\xff\xff',
        "a5a5": {
            "e1e1": b'\xe1\xe1'
        }
    }
}

qpytlv_iostream.write(d)
