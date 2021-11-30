'''
Created on May 9, 2018

@author: xuwang
'''
import cv2
import argparse
import os
import imutils
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcPath", required=True,
    help="source image folder")
ap.add_argument("-t", "--tgtPath", required=True,
    help="target folder to save the maker list")
ap.add_argument("-a", "--angle", required=True,
    help="angle to rotate")
ap.add_argument("-cp", "--cropPercent", required=True, nargs='+',
    help="height and width to crop")
ap.add_argument("-r", "--ratio", required=True,
    help="ratio for shrinking")
args = ap.parse_args()
workingPath = args.srcPath
targetPath = args.tgtPath
ang = float(args.angle)
cp = args.cropPercent
r = float(args.ratio)
# print(float(cp[1]))
imageFiles = os.listdir(workingPath)
rgbIm = []
for im in imageFiles:
    if im.find(".jpg") != -1:
        rgbIm.append(im)
# Detect each individual image
for imf in rgbIm:        
    imgFile = cv2.imread(workingPath+"\\"+imf)
    rotated = imutils.rotate(imgFile, ang)
    imgCrop = rotated[(int(rotated.shape[0]*(float(cp[0])))):(int(rotated.shape[0]*(float(cp[1])))-1), (int(rotated.shape[1]*(float(cp[2])))):(int(rotated.shape[1]*(float(cp[3])))-1)]        
    resizedImage = cv2.resize(imgCrop, (int(imgCrop.shape[1] * r), int(imgCrop.shape[0] * r)), interpolation = cv2.INTER_AREA)
    print(targetPath+"\\"+imf)
    cv2.imwrite(targetPath+"\\"+imf, resizedImage)

