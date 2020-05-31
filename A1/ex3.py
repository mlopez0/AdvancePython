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
import subprocess
import sys

while True:
    print("myshell: ", end="")
    try:
        _input = input()
    except EOFError:
        print()
        exit_terminal()

    if _input == "exit":
        exit_terminal()

    _outcome = subprocess.check_output(_input, shell=True)
    _outcome = str(_outcome).replace('b\'','')#.replace('n\'','')
    outcome = subprocess.run(_input) 
    exitcode = os.system(_input) 
    pid = os.getpid() # collecting Pid
    #exitcode = os.system(_input) # collecting exitcode

    log_string = str(_input) + "-*-" + "xXx args xXx"+ "-*-" + _outcome + '-*-' + str(pid) + "-*-" + str(exitcode)
    action_log(log_string)