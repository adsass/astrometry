#astrometry.py
#max lu

from SIMBAD import Client
from subprocess import *
import os, subprocess, signal, time, sys

#user-adjustable parameters
runTime1 = 60          #Astrometry run-time given object coordinates (s)
runTime2 = 600         #Astrometry run-time without object coordinates (s)
numObjects = 10        #maximum number of SIMBAD objects in a paper to test
radius = 1             #radius from given coordinates (deg)
downsampleFactor = 4   #downsample factor

image = sys.argv[1]

start = time.time()

f = open('outputs/' + image[0:image.rfind('.')] + '.txt','w')
startImage = time.time()
print 'testing image: ' + image
f.seek(0)
f.write('testing image: ' + image + '\n')
#gets list of SIMBAD objects within a paper
SimbadClient = Client()
bibcode = image[0:image.index('-')]
SimbadClient.bibcode = bibcode
SimbadClient.getObjects() 

success = False
ra_dec = ""
#Runs Astrometry on image given SIMBAD coordinates as parameters
if len(SimbadClient.objects)!=0 and len(SimbadClient.objects) <= numObjects:
    for obj in SimbadClient.objects:
        simbadRA = str(obj).split('|')[1]
        simbadDec = str(obj).split('|')[2]
        print 'testing simbad object coordinates: ' + simbadRA + ", " + simbadDec
        if simbadRA != "No Coord.":
            process = subprocess.Popen('solve-field --temp-dir tmp --overwrite --dir astrometry_output --no-plots --downsample ' + str(downsampleFactor) + ' --ra ' + simbadRA + ' --dec ' + simbadDec + ' --radius ' + str(radius) + ' ./images/' + image,stdout=subprocess.PIPE,stderr=STDOUT,shell=True,preexec_fn=os.setsid)
            time.sleep(runTime1)
            try:
                os.killpg(process.pid,signal.SIGTERM)
            except OSError:
                pass
            #Checks to see if Astrometry is successful
            output = process.communicate()[0]
            if output.find('solved')>-1 and output.find('Failed')==-1 and output.find('center')>-1 and output.find('size')>-1:
                success = True
                ra_decIndex = output.find('(RA,Dec)') + 11
                ra_dec = output[ra_decIndex:output.find(') deg.') + 1]
                print 'Image ' + image + ' solved'
                time = (time.time()-startImage)
                f.write("#non-inverted image solved with SIMBAD coordinates in " + str(time) + " seconds\n")
                f.write(ra_dec + '\n')
                f.write(output[output.find('size:') + 6:output.find("Creating new")])
                s = open('solved/' + image[0:image.rfind('.')] + '.out','w')
                s.close()
                break
            elif output.find('Command failed: return value 255')>-1:
                print "Error: " + output
                f.write("Error: \n" + output)
                break

#Runs Astrometry on inverted image given SIMBAD coordinates as parameters            
if success == False:
    if len(SimbadClient.objects)!=0 and len(SimbadClient.objects) <= numObjects:
        print 'testing inverted image: ' + image
        for obj in SimbadClient.objects:
            simbadRA = str(obj).split('|')[1]
            simbadDec = str(obj).split('|')[2]
            print "testing simbad object coordinates: " + simbadRA + ", " + simbadDec
            if simbadRA != "No Coord.":            
                process = subprocess.Popen('solve-field --temp-dir tmp --overwrite --dir astrometry_output --no-plots --downsample ' + str(downsampleFactor) + ' --ra ' + simbadRA + ' --dec ' + simbadDec + ' --radius ' + str(radius) + ' ./images_inverted/' + image,stdout=PIPE,stderr=STDOUT,shell=True,preexec_fn=os.setsid)
                time.sleep(runTime1)
                try:
                    os.killpg(process.pid,signal.SIGTERM)
                except OSError:
                    pass
                #checks to see if Astrometry is successful
                output = process.communicate()[0]
                if output.find('solved')>-1 and output.find('Failed')==-1 and output.find('center')>-1 and output.find('size')>-1:
                    success = True
                    ra_decIndex = output.find('(RA,Dec)') + 11
                    ra_dec = output[ra_decIndex:output.find(') deg.') + 1]
                    print 'Image ' + image + ' solved'
                    time = (time.time()-startImage)
                    f.write("#inverted image solved with SIMBAD coordinates in " + str(time) + " seconds\n")
                    f.write(ra_dec + '\n')
                    f.write(output[output.find('size:') + 6:output.find("Creating new")])
                    s = open('solved/' + image[0:image.rfind('.')] + '.out','w')
                    s.close()
                    break
                elif output.find('Command failed: return value 255')>-1:
                    print "Error: " + output
                    f.write("Error: \n" + output)
                    break                


#Runs istrometry on image without SIMBAD coordinates
if success == False:
    print 'testing image ' + image + " without simbad object coordinates"
    process = subprocess.Popen('solve-field --temp-dir tmp --overwrite --dir astrometry_output --no-plots --downsample ' + str(downsampleFactor) + ' ./images/' + image,stdout=PIPE,stderr=STDOUT,shell=True,preexec_fn=os.setsid)
    time.sleep(runTime2)
    try:
        os.killpg(process.pid,signal.SIGTERM)
    except OSError:
        pass
    output = process.communicate()[0]
    #checks to see if Astrometry is successful
    if output.find('solved')>-1 and output.find('Failed')==-1 and output.find('center')>-1 and output.find('size')>-1:
        success = True
        ra_decIndex = output.find('(RA,Dec)') + 11
        ra_dec = output[ra_decIndex:output.find(') deg.') + 1]
        print 'Image ' + image + ' solved'
        time = (time.time()-startImage)
        f.write("#non-inverted image solved without SIMBAD coordinates in " + str(time) + " seconds\n")
        f.write(ra_dec + '\n')
        f.write(output[output.find('size:') + 6:output.find("Creating new")])
        s = open('solved/' + image[0:image.rfind('.')] + '.out','w')
        s.close()
    elif output.find('Command failed: return value 255')>-1:
        print "Error: " + output
        f.write("Error: \n" + output)

#Runs Astrometry on inverted image without SIMBAD coordinates
if success == False:
    print 'testing inverted image ' + image + " without simbad object coordinates"
    process = subprocess.Popen('solve-field --temp-dir tmp --overwrite --dir astrometry_output --no-plots --downsample ' + str(downsampleFactor) + ' ./images_inverted/' + image,stdout=PIPE,stderr=STDOUT,shell=True,preexec_fn=os.setsid)
    time.sleep(runTime2)
    try:
        os.killpg(process.pid,signal.SIGTERM)
    except OSError:
        pass
    output = process.communicate()[0]
    #checks to see if Astrometry is sucessful
    if output.find('solved')>-1 and output.find('Failed')==-1 and output.find('center')>-1 and output.find('size')>-1:
        success = True
        ra_decIndex = output.find('(RA,Dec)') + 11
        ra_dec = output[ra_decIndex:output.find(') deg.') + 1]
        print 'Image ' + image + ' solved'
        time = (time.time()-startImage)
        f.write("#inverted image solved without SIMBAD coordinates in " + str(time) + " seconds\n")
        f.write(ra_dec + '\n')
        f.write(output[output.find('size:') + 6:output.find("Creating new")])
        s = open('solved/' + image[0:image.rfind('.')] + '.out','w')
        s.close()
    elif output.find('Command failed: return value 255')>-1:
        print "Error: " + output
        f.write("Error: \n" + output)

#Moves images if Astrometry is not successful
if success == False:
    print 'image did not solve'
    f.write('\nimage did not solve')

f.close()
