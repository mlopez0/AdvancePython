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
    act = action.split("-*-")
    dateTimeObj = datetime.now()    
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    file = open("myshell.log", "a")
    file.write("["+ timestampStr +"],"+ " cmd: " + act[0] +", args: "+ act[1] + ", stdout: "+ act[2] + ", Pid: "+  act[3] + ", exit: "+ act[4] +" \n " )
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

    _outcome = subprocess.check_output(_input, shell=True)
    _outcome = str(_outcome).replace('b\'','').replace('\\n\'','')#.replace('x','')

    outcome = subprocess.run(_input) 

    exitcode = os.system(_input) 
    pid = os.getpid() # collecting Pid
    #exitcode = os.system(_input) # collecting exitcode

    log_string = str(_input) + "-*-" + "xXx args xXx"+ "-*-" + _outcome + '-*-' + str(pid) + "-*-" + str(exitcode)
    print ("Cadenota")
    print (log_string)
    action_log(log_string)