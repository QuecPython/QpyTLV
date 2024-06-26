# Import module from usr
from usr.qpytlv import QpyTLV

# Define your tags list or dict if necessary
tags = ['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff', 'a5a5', 'e1e1']

# Create a object of class QpyTLV
tlv = QpyTLV(tags)

# Pack user data as a specific format dict
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

# Build a TLV structure
b = tlv.build(d)
print(b)

# Parse a TLV structure
d = tlv.parse(b)
print(d)
