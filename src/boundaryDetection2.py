'''
Created on May 1, 2020

@author: xuwang
'''
import cv2
import numpy as np
import argparse
import os
import csv
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcPath", required=True,
    help="source image folder")
# ap.add_argument("-t", "--tgtPath", required=True,
#     help="target folder to save the maker list")
args = ap.parse_args()
workingPath = args.srcPath
# targetPath = args.tgtPath
#------------------------------------------------------------------------
imageFiles = os.listdir(workingPath)
rgbIm = []
for im in imageFiles:
    if im.find(".jpg") != -1:
        rgbIm.append(im)
#------------------------------------------------------------------------
# Set final output file name
finalFile = open(workingPath+"\\CanopyCoverRate.csv",'wt')
try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    writer.writerow(('Image_file','Canopy_Rate1','Canopy_Rate2'))
    # Detect each individual image
#     kernel1 = np.ones((3,3),np.uint8)
#     kernel2 = np.ones((7,7),np.uint8)
    for imf in rgbIm:        
        imgFile = cv2.imread(workingPath+"\\"+imf)
        # print("Processing %s" % imf)
        imgHSV = cv2.cvtColor(imgFile, cv2.COLOR_BGR2HSV)
#         cv2.imshow('HSV', imgHSV)
#         cv2.waitKey(0)
        lower_green = np.array([25, 50, 25])
        upper_green = np.array([95, 205, 175])
        maskGreen = cv2.inRange(imgHSV, lower_green, upper_green)
#         cv2.imshow('mask', maskGreen)
#         cv2.waitKey(0)

        midImage = maskGreen[int(maskGreen.shape[0]*0.772)-1:int(maskGreen.shape[0]*0.8)-1,int(maskGreen.shape[1]*0.6)-1:maskGreen.shape[1]-1]
        midImage2 = maskGreen[int(maskGreen.shape[0]*0.2)-1:int(maskGreen.shape[0]*0.227)-1,int(maskGreen.shape[1]*0.6)-1:maskGreen.shape[1]-1]
        plotRateAll = np.sum(midImage/255) / (midImage.shape[0]*midImage.shape[1])
        plotRateAll2 = np.sum(midImage2/255) / (midImage2.shape[0]*midImage2.shape[1])

        writer.writerow((imf, plotRateAll, plotRateAll2))
finally:
    finalFile.close()        
        