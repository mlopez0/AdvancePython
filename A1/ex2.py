'''
Marvin Lopez
Vladimir Semenov

Assignment 1
"Command line hero"

Python 3.8.0
'''

import os


def exit_terminal():
    print("Goodbye!")
    exit()


def handle_cd(input_breakdown):
    if breakdown[0] == "cd":
        path = breakdown[1] if breakdown[0]=="/" else os.path.abspath(breakdown[1]) 
        os.chdir(breakdown[1])
        return True
    
    return False

def get_path_abbreviation(path):
    abbreviated_path = ""
    for directory in path.split("/"):
        if directory == "": continue

        abbreviated_path += "/"
        
        if directory[0] == ".": 
            abbreviated_path += directory[:2]
        else: 
            abbreviated_path += directory[0]
        
    return abbreviated_path

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

    breakdown = _input.split(" ")

    if handle_cd(breakdown):
        continue

    os.system(_input)