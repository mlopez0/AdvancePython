
'''
Marvin Lopez
Vladimir Semenov

Assignment 2
"Russian Hacker"

Python 3.8.0
'''

import dis
import sys
import os
from collections import OrderedDict 
import importlib
import marshal


_nfiles = len(sys.argv)
_files = sys.argv[1:]
#_filesList = {}

header_sizes = [
    # (size, first version this applies to)
    # pyc files were introduced in 0.9.2 way, way back in June 1991.
    (8,  (0, 9, 2)),  # 2 bytes magic number, \r\n, 4 bytes UNIX timestamp
    (12, (3, 6)),     # added 4 bytes file size
    # bytes 4-8 are flags, meaning of 9-16 depends on what flags are set
    # bit 0 not set: 9-12 timestamp, 13-16 file size
    # bit 0 set: 9-16 file hash (SipHash-2-4, k0 = 4 bytes of the file, k1 = 0)
    (16, (3, 7)),     # inserted 4 bytes bit flag field at 4-8 
    # future version may add more bytes still, at which point we can extend
    # this table. It is correct for Python versions up to 3.9
]
header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

if (_nfiles >1):
    #_file = _files[1].replace(".py","")
    _file = _files[1]
    file = open(_file, "rb")
    code = file.read(header_size)
    #code = marshal.load(file)
    file.close()
    dis.dis(code)
#    dis.dis(__import__(_file))

else:
    print ("usage: ex2.py -py src.py")
    print ("This program...")