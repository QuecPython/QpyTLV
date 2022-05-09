#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :TLV.py
@author    :Chavis.Chen (chavis.chen@quectel.com)
@brief     :TLV parsing implemention
@version   :0.1
@date      :2022-05-07 14:02:41
@copyright :Copyright (c) 2022
"""

import ubinascii
from usr.OrderedDict import OrderedDict

#known_tags = ['82', '8A', '95', '9A', '9F10', '9F26', '9F36', '9F37', '9F1A']

emv_tags = {
    '9F01': 'Acquirer Identifier',
    '9F02': 'Amount, Authorised (Numeric)',
    '9F03': 'Amount, Other (Numeric)',
    '9F04': 'Amount, Other (Binary)',
    '9F05': 'Application Discretionary Data',
    '9F06': 'Application Identifier (AID) - terminal',
    '9F07': 'Application Usage Control',
    '9F08': 'Application Version Number',
    '9F09': 'Application Version Number',
    '9F0B': 'Cardholder Name Extended',
    'BF0C': 'FCI Issuer Discretionary Data',
    '9F0D': 'Issuer Action Code - Default',
    '9F0E': 'Issuer Action Code - Denial',
    '9F0F': 'Issuer Action Code - Online',
    '9F10': 'Issuer Application Data',
    '9F11': 'Issuer Code Table Index',
    '9F12': 'Application Preferred Name',
    '9F13': 'Last Online Application Transaction Counter (ATC) Register',
    '9F14': 'Lower Consecutive Offline Limit',
    '9F15': 'Merchant Category Code',
    '9F16': 'Merchant Identifier',
    '9F17': 'Personal Identification Number (PIN) Try Counter',
    '9F18': 'Issuer Script Identifier',
    '9F1A': 'Terminal Country Code',
    '9F1B': 'Terminal Floor Limit',
    '9F1C': 'Terminal Identification',
    '9F1D': 'Terminal Risk Management Data',
    '9F1E': 'Interface Device (IFD) Serial Number',
    '9F1F': 'Track 1 Discretionary Data',
    '5F20': 'Cardholder Name',
    '9F21': 'Transaction Time',
    '9F22': 'Certification Authority Public Key Index',
    '9F23': 'Upper Consecutive Offline Limit',
    '5F24': 'Application Expiration Date',
    '5F25': 'Application Effective Date',
    '9F26': 'Application Cryptogram',
    '9F27': 'Cryptogram Information Data',
    '5F28': 'Issuer Country Code',
    '5F2A': 'Transaction Currency Code',
    '5F2D': 'Language Preference',
    '9F2E': 'Integrated Circuit Card (ICC) PIN Encipherment Public Key Exponent',
    '9F2F': 'Integrated Circuit Card (ICC) PIN Encipherment Public Key Remainder',
    '5F30': 'Service Code',
    '9F32': 'Issuer Public Key Exponent',
    '9F33': 'Terminal Capabilities',
    '5F34': 'Application Primary Account Number (PAN)',
    '9F35': 'Terminal Type',
    '5F36': 'Transaction Currency Exponent',
    '9F37': 'Unpredictable Number',
    '9F38': 'Processing Options Data Object List (PDOL)',
    '9F34': 'Cardholder Verification Method (CVM) Results',
    '9F3A': 'Amount, Reference Currency',
    '9F3B': 'Application Reference Currency',
    '9F3C': 'Transaction Reference Currency Code',
    '9F3D': 'Transaction Reference Currency Exponent',
    '9F40': 'Additional Terminal Capabilities',
    '9F41': 'Transaction Sequence Counter',
    '42': 'Issuer Identification Number (IIN)',
    '9F43': 'Application Reference Currency Exponent',
    '9F44': 'Application Currency Exponent',
    '9F2D': 'Integrated Circuit Card (ICC) PIN Encipherment Public Key Certificate',
    '9F46': 'Integrated Circuit Card (ICC) Public Key Certificate',
    '9F47': 'Integrated Circuit Card (ICC) Public Key Exponent',
    '9F48': 'Integrated Circuit Card (ICC) Public Key Remainder',
    '9F49': 'Dynamic Data Authentication Data Object List (DDOL)',
    '9F4A': 'Static Data Authentication Tag List',
    '9F4B': 'Signed Dynamic Application Data',
    '9F4C': 'ICC Dynamic Number',
    '9F4D': 'Log Entry',
    '9F4E': 'Merchant Name and Location',
    '4F': 'Application Identifier (AID)',
    '50': 'Application Label',
    '9F51': 'Application Currency Code',
    '9F52': 'Card Verification Results (CVR)',
    '5F53': 'International Bank Account Number (IBAN)',
    '5F54': 'Bank Identifier Code (BIC)',
    '5F55': 'Issuer Country Code (alpha2 format)',
    '5F56': 'Issuer Country Code (alpha3 format)',
    '57': 'Track 2 Equivalent Data',
    '9F58': 'Lower Consecutive Offline Limit (Card Check)',
    '9F59': 'Upper Consecutive Offline Limit (Card Check)',
    '5A': 'Application Primary Account Number (PAN)',
    '9F5C': 'Cumulative Total Transaction Amount Upper Limit',
    '9F72': 'Consecutive Transaction Limit (International - Country)',
    '61': 'Application Template',
    '9F65': 'Track 2 Bit Map for CVC3',
    '9F66': 'Track 2 Bit Map for UN and ATC',
    '9F68': 'Mag Stripe CVM List',
    '9F69': 'Unpredictable Number Data Object List (UDOL)',
    '9F6B': 'Track 2 Data',
    '9F6C': 'Mag Stripe Application Version Number (Card)',
    '9F6E': 'Unknown Tag',
    '6F': 'File Control Information (FCI) Template',
    '70': 'EMV Proprietary Template',
    '71': 'Issuer Script Template 1',
    '72': 'Issuer Script Template 2',
    '73': 'Directory Discretionary Template',
    '9F74': 'VLP Issuer Authorization Code',
    '9F75': 'Cumulative Total Transaction Amount Limit - Dual Currency',
    '9F76': 'Secondary Application Currency Code',
    '77': 'Response Message Template Format 2',
    '9F7D': 'Unknown Tag',
    '9F7F': 'Card Production Life Cycle (CPLC) History File Identifiers',
    '80': 'Response Message Template Format 1',
    '81': 'Amount, Authorised (Binary)',
    '82': 'Application Interchange Profile',
    '83': 'Command Template',
    '84': 'Dedicated File (DF) Name',
    '86': 'Issuer Script Command',
    '87': 'Application Priority Indicator',
    '88': 'Short File Identifier (SFI)',
    '89': 'Authorisation Code',
    '8A': 'Authorisation Response Code',
    '8C': 'Card Risk Management Data Object List 1 (CDOL1)',
    '8D': 'Card Risk Management Data Object List 2 (CDOL2)',
    '8E': 'Cardholder Verification Method (CVM) List',
    '8F': 'Certification Authority Public Key Index',
    '90': 'Issuer Public Key Certificate',
    '91': 'Issuer Authentication Data',
    '92': 'Issuer Public Key Remainder',
    '93': 'Signed Static Application Data',
    '94': 'Application File Locator (AFL)',
    '95': 'Terminal Verification Results',
    '97': 'Transaction Certificate Data Object List (TDOL)',
    '98': 'Transaction Certificate (TC) Hash Value',
    '99': 'Transaction Personal Identification Number (PIN) Data',
    '9A': 'Transaction Date',
    '9B': 'Transaction Status Information',
    '9C': 'Transaction Type',
    '9D': 'Directory Definition File (DDF) Name',
    '9F45': 'Data Authentication Code',
    'A5': 'File Control Information (FCI) Proprietary Template',
    '9F57': 'Issuer Country Code',
    '9F39': 'Point-of-Service (POS) Entry Mode',
    '9F73': 'Currency Conversion Factor',
    '9F42': 'Application Currency Code',
    '9F56': 'Issuer Authentication Indicator',
    '9F20': 'Track 2 Discretionary Data',
    'DF01': 'Reference PIN',
    '9F36': 'Application Transaction Counter (ATC)',
    '9F4F': 'Log Format',
    '5F50': 'Issuer URL',
    '9F5A': 'Issuer URL2',
    '9F53': 'Consecutive Transaction Limit (International)',
    '9F54': 'Cumulative Total Transaction Amount Limit',
    '9F55': 'Geographic Indicator'
}


def hexify(number):
    """
    Convert integer to hex string representation, e.g. 12 to '0C'
    """
    if number < 0:
        raise ValueError('Invalid number to hexify - must be positive')

    result = hex(int(number)).replace('0x', '').upper()
    if divmod(len(result), 2)[1] == 1:
        # Padding
        result = '0{}'.format(result)
    return result

def hexstring2bytes(string, byteorder = 'big'):
    if not (type(byteorder) is str and (byteorder == 'big' or byteorder == 'little')):
        raise ValueError('Invalid byteorder:', byteorder)
    string = string.replace('0x', '').replace('0X', '')
    if divmod(len(string), 2)[1] == 1:
        string = '0{}'.format(string)
    return int(string, 16).to_bytes(len(string)//2, byteorder)

def data2hexstring(data):
    if type(data) is str:
        data = data.encode('utf-8')

    if type(data) is bytes or type(data) is bytearray:
        l = ["%02X" % v for v in data]
    else:
        raise TypeError("data must be bytes or bytearray or string.")
    
    return "".join(l)

class TLV:

    def __init__(self, tags=None):
        self.tags = {}

        if tags:
            if type(tags) == list:
                for tag in tags:
                    self.tags[tag] = tag
            elif type(tags) == dict:
                self.tags = tags
            else:
                print('Invalid tags dictionary given - use list of tags or dict as {tag: tag_name}')
        else:
            self.tags = emv_tags

        self.tlv_data = b''
        
        self.tag_lengths = set()
        for tag, tag_name in self.tags.items():
            self.tag_lengths.add(len(tag)//2)


    def parse(self, tlv_data):
        """
        """
        parsed_data = OrderedDict()
        self.tlv_data = tlv_data

        i = 0
        while i < len(self.tlv_data): 
            tag_found = False

            for tag_length in self.tag_lengths:
                for tag_s, tag_name in self.tags.items():
                    try:
                        tag = hexstring2bytes(tag_s)
                    except TypeError:
                        raise ValueError("tag string length must be even.")
                    except ValueError:
                        raise ValueError("tag string must be hex format.")
                    
                    if self.tlv_data[i:i+tag_length] == tag:
                        value_length = self.tlv_data[i+tag_length] << 8 + self.tlv_data[i+tag_length+1]
                        value_start_position = i+tag_length+2
                        value_end_position = i+tag_length+2+value_length

                        if value_end_position > len(self.tlv_data):
                            raise ValueError('Parse error: tag ' + tag_s + ' declared data of length ' + str(value_length) + ', but actual data length is ' + str(int(len(self.tlv_data[value_start_position-1:-1])//2)))

                        value = self.tlv_data[value_start_position:value_end_position]
                        parsed_data[tag_s] = value

                        i = value_end_position
                        tag_found = True

            if not tag_found:
                msg = 'Unknown tag found: ' + str(self.tlv_data[i:i+10])
                raise ValueError(msg)
        return parsed_data


    def build(self, data_dict):
        """
        """
        self.tlv_data = b''
        for tag, value in data_dict.items():
            if not value:
                return self.tlv_data

            value_len = len(value)
            if value_len > 65535:
                raise ValueError("Length of value in TLV is too long ( > 65535).")

            self.tlv_data = self.tlv_data + hexstring2bytes(tag) + hexstring2bytes("%04X" % value_len) + value

        return self.tlv_data
