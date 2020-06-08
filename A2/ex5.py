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
import marshal
import py_compile
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
    print()
    print("print")
    print ("\t" + "-py src.py      produce human-readable bytecode from python file")
    print ("\t" + "-pyc src.pyc    produce human-readable bytecode from compiled .pyc file")
    print ("\t" + "-s \"src\" "+ "\t" +"produce human-readable bytecode from normal string")
    print()
    print("compare -format src [-format src]+")
    print("\tproduce bytecode comparison for giving sources")
    print("\t(supported formats -py, -pyc, -s)")

    exit(2)


def clean_temp_files():
    """Removes __tmp__.py created as temporal code storage for compiling pyc from string"""
    if os.path.exists("__tmp__.py"):
        os.remove("__tmp__.py")


def compile_string(string):
    """Compiles string as out.pyc files"""
    outputFile = "out.pyc"
    subprocess.call('echo "' + string + '" > __tmp__.py', shell=True)
    py_compile.compile("__tmp__.py", outputFile)
    clean_temp_files()


def compile_file(filename):
    """Compiles .pyc out of .py file. Input: <filename>.py"""
    outputFile = filename.split(".")[0] + ".pyc"
    py_compile.compile(filename, outputFile)


def compile_mode(arguments):
    """Pipes to compile functions based on short argument. Throws error if flags are incorrect"""
    if arguments[0] == "-py":
        compile_file(arguments[1])
    elif arguments[0] == "-s":
        compile_string(arguments[1])
    else:
        throw_syntax_error()


def print_instructions(bytecode):
    """Prints list of opnames with its argumnent values"""
    for instruction in bytecode:
        print(instruction.opname, instruction.argval)


def print_py_bc(py_file):
    """Prints opnames and arguments for .py file"""
    code = open(py_file, "r")
    bytecode = dis.Bytecode(code.read())
    code.close()

    print_instructions(bytecode)


def print_pyc_bc(pyc_file):
    """Prints opnames and arguments for .pyc file"""
    file = open(pyc_file, "rb")
    bytecode = file.read(header_size)
    code = marshal.load(file)
    file.close()
    bytecode = dis.Bytecode(code)

    print_instructions(bytecode)


def print_s_bc(string):
    """Prints opnames and arguments for a string"""
    bytecode = dis.Bytecode(string)

    print_instructions(bytecode)


def print_mode(arguments):
    """Pipes to print functions based on short argument. Throws error if flags are incorrect"""
    if arguments[0] == "-py":
        print_py_bc(arguments[1])
    elif arguments[0] == "-pyc":
        print_pyc_bc(arguments[1])
    elif arguments[0] == "-s":
        print_s_bc(arguments[1])
    else:
        throw_syntax_error()


def order_files_by_peaks(table):
    """Returns ordered list of file names based on the peak number of opcode calls"""
    file_peaks = {}

    for file in table.keys():
        file_peaks[file] = max(table[file].values())

    return sorted(file_peaks, key=file_peaks.get)



def compare_mode(files):
    """Creates table of type {filename: {opname: number of occurences}} and pipes it to print function"""
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
    """Creates a beautiful table for number of occurences of opnames in files""" 
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
    """Formats table cell into cell of 'cell_width' symbols (fills with whitespaces or truncates)"""
    return line + (" " * (cell_width - len(line))) if len(line) < cell_width else line[:cell_width]


def parse_options(arguments):
    """Pipes to compile, print or compare mode functions"""
    if arguments[0] == "compile":
        compile_mode(arguments[1:])
    elif arguments[0] == "print":
        print_mode(arguments[1:])
    elif arguments[0] == "compare" and arguments[1] == "-py":
        compare_mode(arguments[2:])
    else:
        throw_syntax_error()

if (len(sys.argv) == 1):
    throw_syntax_error()

parse_options(sys.argv[1:])
