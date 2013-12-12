from subprocess import *
import os, random
import subprocess

totImages = os.listdir('./images/.')
numImages = 1000
testImages = []
imagesLength = str(len(totImages))

i = 0
while i < numImages:
    number = int(random.random()*len(totImages))
    if testImages.count(totImages[number]) == 0:
        testImages.append(totImages[number])
        subprocess.call('cp ' + './images/' + totImages[number] + ' ./testimages/' + totImages[number],shell=True)
        totImages.pop(number)
        i = i+1


