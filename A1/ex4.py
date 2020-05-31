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


error_log = open("myshell.stderr", "w")

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


    try:
        if handle_cd_sp(_input, error_log):
            continue
        output = subprocess.check_call(
            _input, stderr=error_log, shell=True)
    except:
        pass


    

    

