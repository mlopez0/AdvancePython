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
import io

FNULL = open(os.devnull, "w")

_short_flags = "p:s:"

def throw_syntax_error():
    print(sys.argv[0] + " action [-flag value]")
    print("\nThis program ...\n")
    print("compile")
    print("\t-py file.py\tcompile file into bytecode and store it as file.pyc")
    print("\t-s \"src\"\tcompile src into bytecode and store it as out.pyc")
    exit(2)

def clean_temp_files():
    if os.path.exists("__tmp__.py"):
        os.remove("__tmp__.py")


def compile_string(string):
    outputFile = "out.pyc"
    subprocess.call('echo "' + string + '" > __tmp__.py', shell=True)
    py_compile.compile("__tmp__.py", outputFile)
    clean_temp_files()


def compile_file(filename):
    outputFile = filename.split(".")[0] + ".pyc"
    py_compile.compile(filename, outputFile)


def compile_mode(arguments):
    if arguments[0] == "-py":
        compile_file(arguments[1])
    elif arguments[0] == "-s":
        compile_string(arguments[1])
    else:
        throw_syntax_error()


def print_mode(arguments):
    pass


def parse_options(arguments):
    if arguments[0] == "compile":
        compile_mode(arguments[1:])
    elif arguments[0] == "print":
        print_mode(arguments[1:])
    else:
        throw_syntax_error()


if (len(sys.argv) == 1) or sys.argv[1] not in ("compile", "print"):
    throw_syntax_error()


parse_options(sys.argv[1:])
