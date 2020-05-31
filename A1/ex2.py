'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''

import os
from common_functions import * 

dir_path = ""

while True:
    dir_path = get_path_abbreviation(os.getcwd())

    print("myshell [" + dir_path + "]: ", end="")

    try:
        _input = input()
    except EOFError:
        print()
        exit_terminal()

    if _input == "exit":
        exit_terminal()

    if handle_cd(_input):
        continue

    os.system(_input)