#!/bin/bash
#This script gathers a list of images then parses it out to multiple LSF runs.

#This grabs the list of files to work on.  Anything in images is considered a valid file to work on.
filelist=$(ls images6)

#Initialize a few variables. t will store the current file list for the LSF run we are working to generate
t=''

#Counters used to figure out how many files we have looked at for the current file list (i) and how many we have looked at total (j).
i=0
j=0

#Okay, lets actually generate the file list for the runs.
for f in $filelist
do
	#Adds the current file to t.
	t="$t $f"

	#Iterates the counters.
	let i++
	let j++

	#Checks to see if we have enough files in t to work on.  You can adjust this depending on how many files you want each individual run to work on.
	if [ "$i" == "5" ]
	then
		#Submit the run.  What follows is a bash script which actually does the run.
		bsub -n 1 -q normal_serial -o astrometry.out -e astrometry.err -J astrometry "#!/bin/sh
filelist=\"$t\"

#echo \$filelist

for f in \$filelist
do
	python astrometry.py \$f
done"

		#Clear t so we can generate the next file list.
		t=''

		#We also need to clear i so we can start counting again.
		i=0
	fi

	#This will break out of the loop after j number of files have been assigned to be processed.
	#If you want to process all the files then just comment out this section.
	#if [ "$j" == "10" ]
	#then
	#	break
	#fi
done

#There are cases where the number of files may not divide evenly.  So this will submit a final job which contains the remaining files if there are any.
if [ "$i" != "0" ]
then
		bsub -n 1 -q normal_serial -o astrometry.out -e astrometry.err -J astrometry "#!/bin/sh
filelist=\"$t\"

#echo \$filelist

for f in \$filelist
do
	python astrometry.py \$f
done"
fi
