import os
import sys
import subprocess
from datetime import datetime

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

def action_log(action):
     act = action.split("-*-")
     dateTimeObj = datetime.now()    
     timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
     file = open("myshell.log", "a")
     file.write("["+ timestampStr +"],"+ " cmd: " + act[0] +", args: "+ act[1] + ", stdout: "+ act[2] + ", Pid: "+  act[3] + ", exit: "+ act[4] +" \n " )
     file.close()