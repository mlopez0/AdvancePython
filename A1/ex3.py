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


# This function will be moved to common_functions.py
def action_log(action):
    act = action.split(" ")
    var1= "1"
#    print(action.split(" "))
    dateTimeObj = datetime.now()    
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    file = open("myshell.log", "a")
  #  file.write(timestampStr)
    file.write("["+ timestampStr +"],"+ " cmd: " + act[0] +", args: "+ act[1] + ", stdout: "+ var1 + ", Pid: "+  act[2] + ", exit: "+ act[3] +" \n " )
    file.close()

#action_log("echo \"1\" 9444 0")
# Special comands \ " should be scaped 


while True:
    print("myshell: ", end="")

    try:
        _input = input()
    except EOFError:
        print()
        exit_terminal()

    if _input == "exit":
        exit_terminal()

    result = subprocess.check_output(_input, shell=True)
    exitcode = os.system(_input) 
    pid = os.getpid() # collecting Pid
    #exitcode = os.system(_input) # collecting exitcode
    log_string = str(_input) + " " + str(pid) + " " + str(exitcode)
    print ("------------------- log_string ------------------- ls")
    print (log_string)
    print ("subproceso")
    print (result)

    action_log(log_string)