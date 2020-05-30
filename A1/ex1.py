'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''

import os
from common_functions import *


while True:
    print("myshell: ", end="")

    try:
        _input = input()
    except EOFError:
        print()
        exit_terminal()

    if _input == "exit":
        exit_terminal()

    os.system(_input)