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
import py_compile
import getopt

FNULL = open(os.devnull, "w")

_short_flags = "p:"

def check_no_arguments():
    print(sys.argv[0] + " action [-flag value]")
    print("\nThis program ...\n")
    print("compile")
    print("\t-py file.py\tcompile file into bytecode and store it as file.pyc")
    print("\t-s \"src\"\tcompile src into bytecode and store it as out.pyc")
    exit(2)

if (len(sys.argv) == 1) or sys.argv[1] not in ("compile", "print"):
    check_no_arguments()

try:
    arguments, values = getopt.getopt(sys.argv[2:], _short_flags)
    if sys.argv[1] == "compile":
        for argument, value in arguments:
            if argument in ("-p"):
                py_compile.compile(value, value.split(".")[0] + ".pyc")
            elif argument in ("-s"):
                pass
except getopt.GetoptError:
    check_no_arguments()