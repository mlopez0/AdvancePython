'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''

import sys
import os, signal
from io import StringIO
from common_functions import *
import subprocess


# file descriptor for error log
error_log = open("myshell.stderr", "w")

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
    

    try:
        # check if the command is 'cd' 
        # change directory if it is
        # skip actual execution of os.system
        if handle_cd_sp(_input, error_log):
            continue

        # execute command and redirect errors to error log file
        subprocess.check_call(_input, stderr=error_log, shell=True)
    except:
        # ignore actual errors from subprocess so myshell keeps running
        pass


    

    

