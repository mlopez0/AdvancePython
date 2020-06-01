'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Part 3. Hard-boiled sysadmin

Python 3.8.0
'''
import os
from datetime import datetime
from common_functions import get_path_abbreviation, exit_terminal, handle_cd, action_log, build_log_line, get_pid, parse_input
from subprocess import run, PIPE
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

    _command, _argument = parse_input(_input)

    _pid = get_pid(outcome)
    _output_ = outcome.stdout.replace(_pid, '').rstrip().lstrip()        # Return the output
 
    print (_output_)

    action_log(build_log_line(_command, _argument, _output_, _pid, outcome.returncode))

