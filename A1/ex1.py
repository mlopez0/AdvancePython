'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Part 1. "Shell creator"

Python 3.8.0
'''

import os
from A1.common_functions import exit_terminal


while True:
    # show command line prefix
    print("myshell: ", end="")

    # process shell input 
    try:
        _input = input()
    except EOFError:
        # if ctrl+D was pressed input will throw EOFError -> exit terminal
        print() # also go to a new line, since user didn't press return
        exit_terminal()

    if _input == "exit":
        exit_terminal()

    # execute command
    os.system(_input)