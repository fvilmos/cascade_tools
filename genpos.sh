#!/bin/bash

echo "Generates positive pictures from existing positives and negatives"
echo "Parameters: postine width, hight and number of positives to generate"
# celanup
rm -rfv genpos/*

# script parameters
imgw=30
imgh=21

# number of positives forma a single image
nrPos=10

# generate positives for all images from ./genpos folder
FILES="./pos"


# create positive dat file and negative txt file
python3 ./prepare_data.py -posWidthX 80 -posWidthY 60 -negWidthX 160 -negWidthY 120


for f in $FILES/*
do
  # create positives from a single image
  opencv_createsamples -img $f -bg neg.txt -info ./genpos/genpos.dat -pngoutput genpos -maxxangle 1.1 -maxyangle 1.1 -maxzangle 1.1 -num $nrPos -w $imgw -h $imgh
done

#concatenuate the original positives with the generated ones
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
FILEGP='./genpos/genpos.dat'

while read line; do
   # reading each line, append the absolute path and update .dat file
   str=$SCRIPTPATH/pos/$line
   echo $str >> ./info.dat
done < $FILEGP

# copy all generated .jpg files to pos folder
cp ./genpos/*jpg ./pos




