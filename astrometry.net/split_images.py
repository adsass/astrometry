import os
import subprocess
import random

images = os.listdir('./images/')

for i in range(10):
    subprocess.call('mkdir images' + str(i),shell=True)

for image in images:
    dir = random.randint(0,9)
    subprocess.call('touch images' + str(dir) + '/' + image,shell=True)    
