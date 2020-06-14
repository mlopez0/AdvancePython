import dis
import inspect
import bc
import py_compile
import marshal
import sys

""" DON'T MIND THESE COMMENTS, THEY ARE FOR CONVENIENCE """

"""
co_name gives the function name; 
co_argcount is the number of positional arguments (including arguments with default values); 
co_nlocals is the number of local variables used by the function (including arguments); 
co_varnames is a tuple containing the names of the local variables (starting with the argument names); 
co_cellvars is a tuple containing the names of local variables that are referenced by nested functions; 
co_freevars is a tuple containing the names of free variables; 
co_code is a string representing the sequence of bytecode instructions; 
co_consts is a tuple containing the literals used by the bytecode; 
co_names is a tuple containing the names used by the bytecode; 
co_filename is the filename from which the code was compiled; 
co_firstlineno is the first line number of the function; 
co_lnotab is a string encoding the mapping from bytecode offsets to line numbers (for details see the source code of the interpreter); 
co_stacksize is the required stack size (including local variables); 
co_flags is an integer encoding a number of flags for the interpreter.

"""

"""
POP_JUMP_IF_FALSE -> if

16 LOAD_CONST               0 (None)
18 RETURN_VALUE -> added after else

SETUP_FINALLY -> try

POP_EXCEPT -> except

FOR_ITER -> for

SETUP_WITH -> with

MAKE_FUNCTION -> def

LOAD_CONST  N (N)
RETURN_VALUE

or

2x
LOAD_CONST  0 (None)
RETURN_VALUE        -> return

IMPORT_NAME -> import

BINARY_ADD -> +
BINARY_SUBSTRACT -> -
BINARY_TRUE_DIVIDE -> /
BINARY_MULTIPLY -> *

assignment = STORE_NAME - num of def - num of import

and ->
4 LOAD_CONST               1 (1) <- Load const or name twice
6 LOAD_CONST               0 (2)
8 COMPARE_OP               2 (==) <- Compare
10 POP_JUMP_IF_FALSE       26 <- same
12 LOAD_NAME                0 (x)
14 LOAD_CONST               0 (2)
16 COMPARE_OP               2 (==)
18 POP_JUMP_IF_FALSE       26 <- same

COMPARE_OP               (==) <- ==
COMPARE_OP               (!=) <- ==

not switches POP_JUMP_IF_FALSE to opposite
or always have second opname opposite! so it's twice opposite

CALL_FUNCTION  <- calls

"""

import ast


file = open("test.py", "r")
source = file.read()
tree = ast.parse(source)

def get_all(ast_head):
    for branch in ast_head.body:
        try:
            print(branch, type(branch), isinstance(branch, ast.If))
            if isinstance(branch, ast.If):
                print("FOUND IF")
                print(branch.test.op)
                if isinstance(branch.test.op, ast.Or):
                    print("FOUND OR")
                    # And so on, but we need it to be more elegant
            get_all(branch)
        except:
            # Just to see what's going on
            print(branch, branch.__dict__)


print(get_all(tree))
