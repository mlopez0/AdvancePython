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
import py_compile
import marshal
import io
import dis


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


def print_py_bc(py_file):
    code = open(py_file, "r")
    bytecode = dis.Bytecode(code.read())
    code.close()

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)


def print_pyc_bc(pyc_file):
    file = open(pyc_file, "rb")
    bytecode = file.read(header_size)
    code = marshal.load(file)
    file.close()
    bytecode = dis.Bytecode(code)

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)


def print_s_bc(string):
    bytecode = dis.Bytecode(string)

    for instruction in bytecode:
        print(instruction.opname, instruction.argval)


def print_mode(arguments):
    if arguments[0] == "-py":
        print_py_bc(arguments[1])
    elif arguments[0] == "-pyc":
        print_pyc_bc(arguments[1])
    elif arguments[0] == "-s":
        print_s_bc(arguments[1])
    else:
        throw_syntax_error()


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
