# -*- coding: utf-8 -*-

import subprocess
import os
import time

# Define the strings shared between the scripts
pip_address = "169.254.83.74"
python_executable = "c:/Python27/python.exe"

# Define the paths to the scripts
script_path_1 = "c:/Users/ma1177259/GitRepo/sttgoogle-chatgpt/pepperspeechrecognition/module_speechrecognition.py"
script_path_2 = "c:/Users/ma1177259/GitRepo/sttgoogle-chatgpt/peppergpt_module_saveData.py"

# Function to open a new command window and run a command
def run_in_new_console(command):
    cmd = 'start cmd /k "{}"'.format(command)
    subprocess.Popen(cmd, shell=True)

# Construct the commands to be executed in new command windows
command_1 = '{} "{}" --pip {}'.format(python_executable, script_path_1, pip_address)
command_2 = '{} "{}" --pip {}'.format(python_executable, script_path_2, pip_address)

# Run both commands in separate command windows
run_in_new_console(command_1)

time.sleep(4)

run_in_new_console(command_2)

print("Both processes have been started in separate command windows.")
