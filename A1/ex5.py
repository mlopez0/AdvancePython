'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''
import os
from io import StringIO
from common_functions import *
import subprocess


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


    # try:
    #     if handle_cd_sp(_input, error_log):
    #         continue
    #     subprocess.check_call(
    #         _input, stderr=error_log, shell=True)
    # except:
    #     pass

    if _input.split(" ")[0] == "cd":
        path = os.getcwd() + "/" + _input.split(" ")[1]
        if os.path.exists(path):
            current_directory = path
    else:
        subprocess.check_call(
            _input, cwd=current_directory, stderr=error_log)


    

    

