#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :qpytlv-iostream.py
@author    :Chavis.Chen (chavis.chen@quectel.com)
@brief     :TLV data stream io
@version   :0.1
@date      :2022-06-08 16:08:08
@copyright :Copyright (c) 2022
"""

from usr.qpytlv import QpyTLV, QpyTLVError
from usr.TLV import ErrorNo
import _thread

class QpyTLVIOAbs(object):
    def read(self, timeout=0):
        pass

    def write(self, data):
        pass

class QpyTLVIoStream(object):
    def __init__(self, qpytlv, io, parse_cb):
        if not isinstance(qpytlv, QpyTLV):
            raise TypeError("<qpytlv> must be type of QpyTLV.")
        if not isinstance(io, QpyTLVIOAbs):
            raise TypeError("<io> must be type of QpyTLVIOAbs.")
        if not callable(parse_cb):
            raise TypeError("<parse_cb> must be callable.")

        for tag_length in qpytlv._tlv.tag_lengths:
            if tag_length != 2:
                raise QpyTLVError("Tag length is limited to 2 bytes.")

        self._qpytlv = qpytlv
        self._io = io
        self._parse_cb = parse_cb
        self._read_timeout = 100
        _thread.start_new_thread(self._tlv_read_thread, (self,))

    @staticmethod
    def _tlv_read_thread(argv):
        tlv_ios = argv
        data = b''
        parse_pos = 0
        while True:
            data += tlv_ios._io.read(tlv_ios._read_timeout)
            if len(data) >= 4:
                eno, parsed_data = tlv_ios._qpytlv.parse(data)
                tlv_ios._parse_cb(eno, parsed_data)
                if eno == ErrorNo.TAG_ILLEGAL or eno == ErrorNo.TAG_NOT_FOUND:
                    pass
                elif eno == ErrorNo.NO_ERROR:
                    data = b''
                elif eno == ErrorNo.VAL_IS_SHORT:
                    parse_pos = tlv_ios._qpytlv.get_parse_position()
                    data = data[parse_pos:]
                else:
                    raise QpyTLVError("Unknown error.")

    def write(self, data):
        w_data = self._qpytlv.build(data)
        self._io.write(w_data)
