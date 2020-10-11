#! /usr/bin/python
from datetime import datetime
import cv2
import numpy as np
import argparse
import os


# input arguments
parser = argparse.ArgumentParser(description='Simple annotation tool \n \
    Use "a" to start annotate, ENTER to return \n')
parser.add_argument('-cam', type=int, help='Camera index', default=1)
parser.add_argument('-vid', type=str, help='Video file', default='')

args = parser.parse_args()
path, filename = os.path.split(os.path.realpath(__file__))

# select video or camera
if  args.vid != '':
    cap = cv2.VideoCapture(args.vid)
else:
    cap = cv2.VideoCapture(args.cam)

roi = []
frame = np.array((480,640,3), dtype=np.uint8)
img = np.array((120,160,3), dtype=np.uint8)
ccount = 0

cv2.namedWindow('annotate')
cv2.namedWindow('capture')


while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    
    k = cv2.waitKey(10)
    
    # quit on ESC key
    if k == 27:
        cv2.destroyAllWindows()
        exit()

    #start annotation, save file with timestamp
    if k== ord('a'):
        roi = cv2.selectROI('annotate',frame)
        img = frame[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]

        now = datetime.now()
        ts = datetime.timestamp(now)

        cv2.imwrite(path +'/raw/'+ 'img_' + str(int(ts)) + '.jpg', img)
        
        ccount +=1
        print ("Capture count:" + str(ccount))


    cv2.imshow('capture',img)
    cv2.imshow('annotate',frame)

cap.close()
cv2.destroyAllWindows()
