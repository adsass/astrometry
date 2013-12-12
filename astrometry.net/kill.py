import subprocess, sys

for i in range(int(sys.argv[1]), int(sys.argv[2])):
    subprocess.call('bkill ' + str(i), shell=True) 
