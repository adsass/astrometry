This directory contains the scripts that were run on the Odyssey cluster (odyssey.fas.harvard.edu) in order to extract and astrometrically calibrate images from a batch of 56,000 articles from ADS. A total of ~200,000 images were extracted from the papers. Roughly 3,500 images were solved by astrometry.net.

## Odyssey server instructions

First, ssh into the server at ``legacy.rc.fas.harvard.edu``. Images and scripts can be found at (temporary): ``/n/scratch2/goodman_lab/maxlu``. To load astrometry run ``module load hpc/astrometry-0.40``. Run astrometry with ``solve-field --downsample 4 (image)``.

## How to extract images from a folder of PDFs

Run script ``imageextract.py``. It:
1. extracts images from pdfs in a folder named ``papers`` into a folder named ``raw_images`` 
2. takes those pictures and converts them into pngs in a folder named ``converted_images``
3. copies them into a folder named ``converted_images_inverted`` and inverts them.

## How to calibrate images using astrometry

1. Load the pyfits module with command: ``module load hpc/pyfits-3.0.8_python-2.7.1``
2. remove the tmp directory
3. make a new tmp directory
4. edit line 5 of launcher.sh to list the appropriate image directory (ex ``filelist=$(ls images5)``)
5. run using command: ``bsub < launcher.sh``

You can track the progress of your jobs using the command ``bjobs``. It will take a few hours for the job to actually launch onto the cluster. Once done, the image metadata will be stored in the outputs directory, and a list of all solved images will be updated in the solved directory.

