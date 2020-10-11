#!/usr/bin/env python3

import cv2
import numpy as np
import sys
import os
import time
import glob
import argparse

# input arguments
parser = argparse.ArgumentParser(description='Prepar dataset for Cascade trainer.\n Defaults: posWidthX=50, posWidthY=50, negWidthX=100, negWidthY=100, location /pos/*.*, /neg/*.*')
parser.add_argument('-posWidthX', type=int, help='Positive sample x Width', default=80)
parser.add_argument('-posWidthY', type=int, help='Positive sample y Width', default=60)

parser.add_argument('-negWidthX', type=int, help='Negative sample x Width', default=160)
parser.add_argument('-negWidthY', type=int, help='Negative sample y Width', default=120)

parser.add_argument('-pos', type=str, help='Positive samples location', default='/pos/*.*')
parser.add_argument('-neg', type=str, help='Negative samples location', default='/neg/*.*')

args = parser.parse_args()

# sample sizes
POS_SIZE=(args.posWidthX,args.posWidthY)
NEG_SIZE = (args.negWidthX,args.negWidthY)

# current path
path, filename = os.path.split(os.path.realpath(__file__))

# read files
pfiles = glob.glob(path + args.pos)
nfiles = glob.glob(path + args.neg)


# check directory structure
if len(pfiles)== 0:
    print ('no positive images found, check pos dir!')
    exit
if len(nfiles)== 0:
    print ('no negative images found, check neg dir!')
    exit

# create positive images descriptor
f = open(path +'/info.dat','x')

for pf in pfiles:

    # create tag to write in info.dat =>  objnr=1 startx=0 starty=0 endx=50 endy=50
    infoline = pf + ' 1 0 0 ' + str(POS_SIZE[0]) + ' ' + str(POS_SIZE[1]) +'\n'
    
    f.write(infoline)
    
    # resize img to desired size
    img = cv2.imread(pf)
    h,w = img.shape[:2]

    # resize if picture dimensiona are different
    if (w,h) != POS_SIZE:
        img = cv2.resize(img,POS_SIZE)
        try:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)
        except:
            pass
        cv2.imwrite(pf,img)

f.close()

# create negative images descriptor
f = open(path +'/neg.txt','x')

for nf in nfiles:
 
    f.write(nf + '\n')

    img = cv2.imread(nf)
    h,w = img.shape[:2]
    
    # resize if picture dimensiona are different
    if (w,h) != NEG_SIZE:
        img = cv2.resize(img,NEG_SIZE)
        try: 
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)
        except:
            pass

        cv2.imwrite(nf,img)
f.close()
