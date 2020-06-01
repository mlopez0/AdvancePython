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

    outcome = run(_input, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    # pid = Popen("ls") # must be changed
    pid = 1

    '''    print ("This is the comand \t" + str(_input))
        print ("These are the args \t" + outcome.args)
        print ("This is the output \t " + outcome.stdout)
        print ("This is the exit code \t" + str(outcome.returncode))
    '''
    log_string = str(_input) + "-*-" + outcome.args + "-*-" + outcome.stdout + '-*-' + str(pid) + "-*-" + str(outcome.returncode)
    action_log(log_string)