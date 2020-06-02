'''
Marvin Lopez
Vladimir Semenov

Assignment 2
"Russian Hacker"

Python 3.8.0
'''
import time
import sys
import os
from collections import OrderedDict 

_nfiles = len(sys.argv)
_files = sys.argv[1:]
_filesList = {}

for i in _files:
    start = time.time()
    os.system("python " + str(i))
    end = time.time()
    elapsed = end - start
    _filesList[i] = elapsed

i=1

print ("PROGRAM \t| RANK \t| TIME LAPSED")
for key, value in sorted(_filesList.items(), key=lambda item: item[1]):
    print("%s \t %i \t %s" % (key, i, value))
    i = i+1


