import os

def exit_terminal():
    print("Goodbye!")
    exit()


def handle_cd(input_breakdown):
    if breakdown[0] == "cd":
        path = breakdown[1]
        
        try:
            exit_code = os.chdir(path)
        except FileNotFoundError:
            log_error("/bin/sh: 1: cd: can't cd to " + path)
    
    return -1


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