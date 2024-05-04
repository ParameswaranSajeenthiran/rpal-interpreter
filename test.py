import subprocess
import os
# Arguments to be passed to the called script
arg1 = "test_cases/test"
dir=os.listdir("test_cases")
for file in dir :
    # print("output for file: ", file ,end=" ")
    subprocess.run(['python', 'myrpal.py', "test_cases\\"+ file])


# Run the called script with arguments
