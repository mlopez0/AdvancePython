
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


if (_nfiles >1):
    _file = _files[1].replace(".py","")
    dis.dis(__import__(_file))

else:
    print ("usage: ex2.py -py src.py")
    print ("This program...")