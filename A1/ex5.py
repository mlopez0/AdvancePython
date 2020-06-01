'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''
import os
from io import StringIO
from A1.common_functions import get_path_abbreviation, exit_terminal, handle_cd_sp, action_log
from subprocess import run, PIPE


error_log = open("myshell.stderr", "w")
current_directory = os.getcwd()

dir_path = ""


while True:
    dir_path = get_path_abbreviation(current_directory)

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
    except:
        pass
