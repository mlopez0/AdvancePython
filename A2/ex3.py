
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
import marshal
from collections import OrderedDict 
import importlib

_nfiles = len(sys.argv)
_files = sys.argv[1:]
_filesList = {}

_opt = _files[0]
_args = _files[1]
_file = _files[1]

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

if _opt == "-py":
    _file = _files[1]
    code = open(_file, "r")
    bytecode = dis.Bytecode(code.read())
    code.close()

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)

elif _opt == "-pyc": 
    _file = _files[1]
    file = open(_file, "rb")
    bytecode = file.read(header_size)
    code = marshal.load(file)
    file.close()
    bytecode = dis.Bytecode(code)

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)

elif _opt == "-s": 
    bytecode = dis.Bytecode(_file)

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)


else:
    print ("usage: ex2.py -formay src")
    print ("This program ...")
    print ("\t" + "-py src.py      produce human-readable bytecode from python file")
    print ("\t" + "-pyc src.pyc    produce human-readable bytecode from compiled .pyc file")
    print ("\t" + "-s \"src\" "+ "\t" +"produce human-readable bytecode from normal string")

