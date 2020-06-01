'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Part 4. CCleaner

Python 3.8.0
'''
import os
from datetime import datetime
from common_functions import get_path_abbreviation, exit_terminal, handle_cd_sp, action_log, error_logger, parse_input, get_pid, build_log_line
from subprocess import check_call, PIPE, run
import sys

dir_path = ""
# file descriptor for error log
error_log = open("myshell.stderr", "w")

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
        # check if the command is 'cd' 
        # change directory if it is
        # skip actual execution of os.system
        if handle_cd_sp(_input, error_log):
            continue
    except:
        # ignore actual errors from subprocess so myshell keeps running
        pass


    outcome = run(_input + " & echo $!", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    _error = str(outcome.stderr)

    if (not _error ):
        
        _command, _argument = parse_input(_input)

        _pid = get_pid(outcome)
        _output_ = outcome.stdout.replace(_pid, '').rstrip().lstrip()         # Return the output
 
        print (_output_)
    
        action_log(build_log_line(_command, _argument, _output_, _pid, outcome.returncode))
    else:
        error_logger(_error, error_log)