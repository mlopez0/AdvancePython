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
import dis

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
    # TODO: Rewrite manually from ex3
    pass


def order_files_by_peaks(table):
    file_peaks = {}

    for file in table.keys():
        file_peaks[file] = max(table[file].values())

    return sorted(file_peaks, key=file_peaks.get)



def compare_mode(files):
    table = {filename: {} for filename in files}

    for file in files:
        code = open(file, "r")
        bytecode = dis.Bytecode(code.read())
        code.close()
        
        for instr in bytecode:
            same_opnames = [instruction.opname for instruction in bytecode if instruction.opname == instr.opname]
            table[file][instr.opname] = len(same_opnames)
    
    print_table(table)


def print_table(table_dict):
    opnames = set().union(*[opnames for opnames in table_dict.values()])
    files_in_order = order_files_by_peaks(table_dict)
    print(fill("INSTRUCTION"), end="")
    for filename in files_in_order:
        print(fill("| " + filename), end="")

    print()
    
    for opname in opnames:
        print(fill(opname), end="")
        for filename in table_dict.keys():
            num = "0"
            if opname in table_dict[filename].keys():
                num = str(table_dict[filename][opname])
            print(fill("  " + num), end="")

        print()

def fill(line, cell_width=13):
    return line + (" " * (cell_width - len(line))) if len(line) < cell_width else line[:cell_width]


def parse_options(arguments):
    if arguments[0] == "compile":
        compile_mode(arguments[1:])
    elif arguments[0] == "print":
        print_mode(arguments[1:])
    elif arguments[0] == "compare" and arguments[1] == "-py":
        compare_mode(arguments[2:])
    else:
        throw_syntax_error()


if (len(sys.argv) == 1) or sys.argv[1] not in ("compile", "print", "compare"):
    throw_syntax_error()


parse_options(sys.argv[1:])
