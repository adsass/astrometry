#!/bin/bash

filelist=$(cat file1.txt)

echo $filelist

for f in $filelist
do
	echo "python astrometry.py $f"
	python astrometry.py $f
done
