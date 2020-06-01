'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''
import os
from datetime import datetime
from common_functions import *
from subprocess import *
import sys

''' command name | arguments | lines of output | pid | exit code '''

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

    outcome = run(_input + " & echo $!", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

    _command = _input.split(' ', 1)[0]                  # Return the command 

    try:
        _argument = _input.split(' ', 1)[1]             # Return the command arguments
    except IndexError:
        _argument = '-'
    _pid = outcome.stdout.partition('\n')[0]            # Return the Pid
    _output_ = outcome.stdout.replace(_pid, '')         # Return the output
 
    print (_output_)


    
    log_string = _command + "-*-" + _argument + "-*-" + _output_.rstrip().lstrip() + '-*-' + _pid + "-*-" + str(outcome.returncode)

    action_log(log_string)