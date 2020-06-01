'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Part 2. Path Screwer

Python 3.8.0
'''

import os
from A1.common_functions import get_path_abbreviation, exit_terminal, handle_cd


# path displayed after 'myshell' prefix
dir_path = ""


while True:
    # get current path and abbreviate it
    dir_path = get_path_abbreviation(os.getcwd())
    
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
    
    # check if the command is 'cd' 
    # change directory if it is
    # skip actual execution of os.system
    if handle_cd(_input):
        continue

     # execute command
    os.system(_input)