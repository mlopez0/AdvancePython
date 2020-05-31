import os
import sys
import subprocess

def exit_terminal():
    print("Goodbye!")
    exit()


def handle_cd(_input):
    input_breakdown = _input.split(" ")

    if input_breakdown[0] == "cd":
        path = input_breakdown[1]
        
        os.chdir(path)
        return True
    
    return False


def handle_cd_sp(_input, error_out=sys.__stderr__):
    input_breakdown = _input.split(" ")

    if input_breakdown[0] == "cd":
        path = input_breakdown[1]
        
        error_out.seek(0)
        error_out.truncate(0)

        subprocess.check_output(_input, shell=True, stderr=error_out)
        os.chdir(path)

        return True
    
    return False


def log_error(error):
    file = open("myshell.stderr", "w+")
    file.write(error + "\n")
    file.close()


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


def print_stdout(message, stdout, current_stdout, **options):
    sys.stdout = stdout
    print(message, **options)