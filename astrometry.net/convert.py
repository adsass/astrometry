import os,subprocess
for image in os.listdir('./testimages/.'):
    subprocess.call('convert ./testimages/' + image + ' ./testimagespng/' + image.replace('.ppm','.png'),shell=True)
