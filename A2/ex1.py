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
import subprocess
from collections import OrderedDict 

FNULL = open(os.devnull, "w")

_nfiles = len(sys.argv)
_files = sys.argv[1:]
_filesList = {}

check_no_arguments()

for i in _files:
    start = time.time()
    # os.system("python3 " + str(i))
    subprocess.call("python3 " + str(i), stdout=FNULL, cwd=os.getcwd(), shell=True)
    # subprocess.run("ls")
    end = time.time()
    elapsed = end - start
    _filesList[i] = elapsed

i=1

print ("PROGRAM \t| RANK \t| TIME LAPSED")
for key, value in sorted(_filesList.items(), key=lambda item: item[1]):
    print("%s \t %i \t %s" % (key, i, value))
    i = i+1


def check_no_arguments():
    if _nfiles == 1:
        print("usage: python3 " + sys.argv[0] + " [files]")
        print("This program ...\n")
        exit()