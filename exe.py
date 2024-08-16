# -*- coding: utf-8 -*-

import subprocess

# Define the strings shared between the scripts
pip_address = "169.254.126.93"
python_executable = "c:/Python27/python.exe"

# Define the paths to the scripts
script_path_1 = "c:/Users/ma1177259/GitRepo/sttgoogle-chatgpt/pepperspeechrecognition/module_speechrecognition.py"
script_path_2 = "c:/Users/ma1177259/GitRepo/sttgoogle-chatgpt/peppergpt_module_saveData.py"

# Construct the commands to be executed
command_1 = [python_executable, script_path_1, "--pip", pip_address]
command_2 = [python_executable, script_path_2, "--pip", pip_address]

# Execute the commands in separate consoles (using subprocess.Popen)
process_1 = subprocess.Popen(command_1, shell=True)
process_2 = subprocess.Popen(command_2, shell=True)

# Wait for both processes to complete
while process_1.poll() is None or process_2.poll() is None:
    # Poll() returns None if the process is still running
    # This loop will continue until both processes are done
    continue

# Both processes are now finished
print("Both processes have completed.")