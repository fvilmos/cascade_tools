#!/bin/bash

echo "Create vector file from positives, negatives and starts the training"
echo "Parameters: posivies size, number of posties, "


# Number of training stages
nrStages=20

# detection types [HAAR,LBP]
fn=HAAR
# object size, width, height
imgw=30
imgh=21

# number of images containg the object to detect (see pos directory content)
nrf=0
FILES=./pos/*.jpg
for f in $FILES; do
  nrf=$((nrf+1))
done

nrPos=$nrf

# number of images NOT containg the object to detect (see neg directory content)
nrf=0
FILES=./pos/*.jpg
for f in $FILES; do
  nrf=$((nrf+1))
done

nrNeg=$nrf

# create positive dat file and negative txt file
python3 ./prepare_data.py -posWidthX 80 -posWidthY 60 -negWidthX 160 -negWidthY 120

# create vector file from positives
opencv_createsamples -info info.dat -vec positives.vec -bg neg.txt -maxxangle 1.1 -maxyangle 1.1 -maxzangle 1.1 -w $imgw -h $imgh

# create positives from a single image
#opencv_createsamples -img object.jpg -bg neg.txt -info info/info.lst -pngoutput info -maxxangle 1.1 -maxyangle 1.1 -maxzangle 1.1 -num $nrPos -w $imgw -h $imgh


# train cascade
opencv_traincascade -data ./data -vec positives.vec -bg neg.txt -numPos $nrPos -numNeg $nrNeg -numStages $nrStages -w $imgw -h $imgh -minHitRate 0.999 -maxFalseAlarmRate 0.5 -mode ALL -numThreads 8 -featureType $fn -precalcValBufSize 1024 -precalcIdxBufSize 1024
