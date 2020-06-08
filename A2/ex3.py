
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

_nfiles = len(sys.argv)
_files = sys.argv[1:]
_filesList = {}

_opt = _files[0]
_args = _files[1]
_file = _files[1]


if _opt == "-py":
    _file = _files[1].replace(".py","")
    bytecode = dis.dis(_file)
elif _opt == "-pyc": 
    _file = _files[1].replace(".pyc","")
    bytecode = dis.dis(_file)
elif _opt == "-s": 
    bytecode = dis.dis(_file)
else:
    print ("usage: ex2.py -formay src")
    print ("This program ...")
    print ("\t" + "-py src.py      produce human-readable bytecode from python file")
    print ("\t" + "-pyc src.pyc    produce human-readable bytecode from compiled .pyc file")
    print ("\t" + "-s \"src\" "+ "\t" +"produce human-readable bytecode from normal string")

