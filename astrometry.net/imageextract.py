#imageextract.py
#max lu

import os, subprocess, time
from pyPdf import PdfFileReader

start = int(round(time.time()*1000))
subprocess.call('rm ' + './papers/.DS_Store', shell=True)
subprocess.call('rm ' + './raw_images/.DS_Store', shell=True)
subprocess.call('rm ' + './converted_images/.DS_Store', shell=True)
subprocess.call('rm ' + './converted_images_inverted/.DS_Store', shell=True)


#extracts images from pdfs in papers
startExtract = int(round(time.time()*1000))
for filename in os.listdir('./papers/.'):
    if str(filename).strip().find(".pdf")>-1:
        bibcode = filename.replace(".pdf","")
        subprocess.call('pdfimages -p ' + "./papers/" + filename + " raw_images/" + bibcode,shell=True)
stopExtract = int(round(time.time()*1000))
print "Extraction time: " + str(stopExtract - startExtract) + "ms"
print ""


#removes pdf page images
startPageRemove = int(round(time.time()*1000))
for filename in os.listdir('./papers/.'):
    f = filename.replace(".pdf","")
    pageNumbers = []
    images = []
    imagesCopy = []

    #counts number of pages in pdf
    pageNumber = PdfFileReader(file("./papers/" + filename,"rb")).getNumPages()

    #checks to see if document is unlayered    
    isUnlayered = True
    for image in os.listdir('./raw_images/.'):
        if f in image:
            pageNumbers.append(int(image[len(image)-11:len(image)-8]))
            images.append(image)
    for i in range(pageNumber + 1):
        if i!=0 and pageNumbers.count(i)==0:
            isUnlayered = False
    #deletes pages that do not contain an image
    if isUnlayered:
        imagesCopy = images
        for i in range(pageNumber + 1):
            if pageNumbers.count(i) == 1:
                index = pageNumbers.index(i)
                subprocess.call('rm ' + './raw_images/' + images[images.index(imagesCopy[index])], shell=True)

        #deletes pages from which images have been extracted
        pages = []
        removedImages = []
        for extractedImage in os.listdir('./raw_images/.'):
            if f in extractedImage and pages.count(extractedImage[len(extractedImage)-11:len(extractedImage)-8]) == 0:
                pages.append(extractedImage[len(extractedImage)-11:len(extractedImage)-8])
    
        for pageString in pages:
            extractedImages = []
            for img in os.listdir('./raw_images/.'):
                if f + "-" + pageString in img:
                    extractedImages.append(img)
            removedImages.append(extractedImages.pop())

        for removedImage in removedImages:
            subprocess.call('rm ' + './raw_images/' + removedImage,shell=True)
stopPageRemove = int(round(time.time()*1000))
print "Page Removal time: " + str(stopPageRemove - startPageRemove) + "ms"
print ""


#converts images in raw_images from ppm or pbm to png
startConvert = int(round(time.time()*1000))
for filename in os.listdir('./raw_images/.'):
    if os.stat('./raw_images/' + filename).st_size >= 640:  
        if str(filename).strip().find(".ppm")>-1:
            subprocess.call('convert ' + "./raw_images/" + filename + " converted_images/" + filename.replace(".ppm",".png"),shell=True)

        elif str(filename).strip().find(".pbm")>-1:
            subprocess.call('convert ' + "./raw_images/" + filename + " converted_images/" + filename.replace(".pbm",".png"),shell=True)
stopConvert = int(round(time.time()*1000))
print "Convert time: " + str(stopConvert - startConvert) + "ms"
print ""


#inverts files in converted_images, copies to converted_images_inverted
startInvert = int(round(time.time()*1000))
for filename in os.listdir('./converted_images/.'):  
    subprocess.call('convert ' + "./converted_images/" + filename + " -negate " + "./converted_images_inverted/" + filename.replace(".png","_inverted.png"), shell=True)
stopInvert = int(round(time.time()*1000))
print "Invert time: " + str(stopInvert - startInvert) + "ms"
print ""

end = int(round(time.time()*1000))
print "Elapsed time: " + str(end - start) + "ms"
