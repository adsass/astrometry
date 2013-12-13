This directory contains the scripts that were run on the Odyssey cluster (odyssey.fas.harvard.edu) in order to extract and astrometrically calibrate images from a batch of 56,000 articles from ADS. A total of ~200,000 images were extracted from the papers. Roughly 3,500 images were solved by astrometry.net.

## Odyssey server instructions

**To load astrometry run**
module load hpc/astrometry-0.40

**Run astrometry with**
solve-field --downsample 4 (image)
