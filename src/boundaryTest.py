'''
Created on Jun 13, 2018

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
r=0.25
try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    writer.writerow(('Image_file','Canopy_Rate_Index','Canopy_Rate'))
    # Detect each individual image
    kernel1 = np.ones((3,3),np.uint8)
    kernel2 = np.ones((7,7),np.uint8)
    for imf in rgbIm:        
        imgFile = cv2.imread(workingPath+"\\"+imf)
        print("Processing %s" % imf)
        resizedImage = cv2.resize(imgFile, (int(imgFile.shape[1] * r), int(imgFile.shape[0] * r)), interpolation = cv2.INTER_AREA)
        imgHSV = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2HSV)
        cv2.imshow('HSV', imgHSV)
        cv2.waitKey(0)
#         lower_green = np.array([22, 50, 50]) #35
#         upper_green = np.array([52, 205, 205]) #95
        lower_green = np.array([0, 0, 0])
        upper_green = np.array([5, 255, 255])
        maskGreen = cv2.inRange(imgHSV, lower_green, upper_green)
        cv2.imshow('mask', maskGreen)
        cv2.waitKey(0)
        # Smooth (blur) images
        blurred = cv2.bilateralFilter(maskGreen,7,80,80)
        cv2.imshow('Blurred', blurred)
        cv2.waitKey(0)
        # Binary 
        thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        cv2.imshow('Binary', thresh)
        cv2.waitKey(0)
        # ---------------------------------------------------------------------------------
        # Create a kernel
        dilation = cv2.dilate(thresh,kernel1,iterations = 1)
        cv2.imshow('Dilation', dilation)
        cv2.waitKey(0)
        opened = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel1)
        cv2.imshow('Opened', opened)
        cv2.waitKey(0)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel1)
        cv2.imshow('Closed', closed)
        cv2.waitKey(0)
        erosion = cv2.erode(closed,kernel1,iterations = 1)
        cv2.imshow('Erosion', erosion)
        cv2.waitKey(0)
        # Use opening to fill the blobs
        opened = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel2)
        # Use closing to disconnect the bridges
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)
        # Use opening to fill the blobs
        opened = cv2.morphologyEx(opened, cv2.MORPH_OPEN, kernel2)
        # Use closing to disconnect the bridges
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)
        cv2.imshow('Processed', closed)
        cv2.waitKey(0)
        plotRateAll = np.sum(closed/255) / (closed.shape[0]*closed.shape[1])          
#         #---------------------------------------------------
#         # Top
#         topImage = closed[int(closed.shape[0]*0.05)-1:int(closed.shape[0]*0.3)-1,0:closed.shape[1]-1]
#         topRate = np.sum(topImage/255) / (topImage.shape[0]*topImage.shape[1])
#         if topRate >= 0.5:
#             topRate = 1
#         else:
#             topRate = 0 
#         #---------------------------------------------------
#         # Center
#         midImage = closed[int(closed.shape[0]*0.45)-1:int(closed.shape[0]*0.55)-1,0:closed.shape[1]-1]
#         midRate = np.sum(midImage/255) / (midImage.shape[0]*midImage.shape[1])
#         if midRate >= 0.5:
#             midRate = 1
#         else:
#             midRate = 0
#         #---------------------------------------------------
#         # Bottom
#         bottomImage = closed[int(closed.shape[0]*0.65)-1:int(closed.shape[0]*0.95)-1,0:closed.shape[1]-1]
#         bottomRate = np.sum(bottomImage/255) / (bottomImage.shape[0]*bottomImage.shape[1])
#         if bottomRate >= 0.5:
#             bottomRate = 1
#         else:
#             bottomRate = 0
#         #---------------------------------------------------
#         if topRate == 0 and midRate == 0 and bottomRate == 0:
#             plotRate = 0
#         elif topRate == 0 and midRate == 0 and bottomRate == 1:
#             plotRate = 0
#         elif topRate == 0 and midRate == 1 and bottomRate == 0:
#             plotRate = 0
#         elif topRate == 0 and midRate == 1 and bottomRate == 1:
#             plotRate = 1
#         elif topRate == 1 and midRate == 0 and bottomRate == 0:
#             plotRate = 0
#         elif topRate == 1 and midRate == 0 and bottomRate == 1:
#             plotRate = -1
#         elif topRate == 1 and midRate == 1 and bottomRate == 0:
#             plotRate = 1
#         else:
#             plotRate = 1
        #---------------------------------------------------
        # Top
        topImage = closed[int(closed.shape[0]*0.05)-1:int(closed.shape[0]*0.35)-1,0:closed.shape[1]-1]
        topRate = np.sum(topImage/255) / (topImage.shape[0]*topImage.shape[1])
        #---------------------------------------------------
        # Center
        midImage = closed[int(closed.shape[0]*0.45)-1:int(closed.shape[0]*0.55)-1,0:closed.shape[1]-1]
        midRate = np.sum(midImage/255) / (midImage.shape[0]*midImage.shape[1])
        #---------------------------------------------------
        # Bottom
        bottomImage = closed[int(closed.shape[0]*0.65)-1:int(closed.shape[0]*0.95)-1,0:closed.shape[1]-1]
        bottomRate = np.sum(bottomImage/255) / (bottomImage.shape[0]*bottomImage.shape[1])
        #---------------------------------------------------    
        avgRate = np.average([topRate,midRate,bottomRate])
        if topRate >= avgRate:
            topRateV = 1
        else:
            topRateV = 0
        if midRate >= avgRate:
            midRateV = 1
        else:
            midRateV = 0
        if bottomRate >= avgRate:
            bottomRateV = 1
        else:
            bottomRateV = 0 
        #---------------------------------------------------
        if topRateV == 0 and midRateV == 0 and bottomRateV == 0:
            plotRate = avgRate
        elif topRateV == 0 and midRateV == 0 and bottomRateV == 1:
            plotRate = avgRate
        elif topRateV == 0 and midRateV == 1 and bottomRateV == 0:
            plotRate = avgRate
        elif topRate == 0 and midRateV == 1 and bottomRateV == 1:
            plotRate = 1
        elif topRateV == 1 and midRateV == 0 and bottomRateV == 0:
            plotRate = avgRate
        elif topRateV == 1 and midRateV == 0 and bottomRateV == 1:
            plotRate = -1
        elif topRateV == 1 and midRateV == 1 and bottomRateV == 0:
            plotRate = 1
        else:
            plotRate = 1
        #---------------------------------------------------
        writer.writerow((imf, plotRate, plotRateAll))
finally:
    finalFile.close()        
        