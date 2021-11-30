'''
Created on Jan 16, 2021

@author: xuwang
'''
import os
import argparse
import cv2
# ------------------------------------------------------------------------
ap = argparse.ArgumentParser()
# ==============
ap.add_argument("-s", "--sPath", required=True,
                help="source folder")
ap.add_argument("-t", "--tPath", required=True,
                help="target folder")
# ==============
args = ap.parse_args()
sPath = args.sPath
tPath = args.tPath
bp = 0.5
# ------------------------------------------------------------------------
exten = 'tif'
imList = []

for dirpath, dirnames, files in os.walk(sPath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
for img in imList:
    if os.path.isfile(img):
        imgFileProcessing = cv2.imread(img)
        y1 = int(imgFileProcessing.shape[0] * float(bp)) - 256
        y2 = y1 + 512
        x_min = int(imgFileProcessing.shape[1] / 16)
        x_max = int(imgFileProcessing.shape[1] / 16 * 15)
        imgFileName = img.split("\\")[-1]
        imgPart = imgFileName.split("_")
        for xi in range(x_min, x_max, 512):
            imgCrop = imgFileProcessing[y1:y2, xi:xi + 512]
            imf = imgPart[0] + "_" + imgPart[1] + "_" + imgPart[2] + "_" + imgPart[3] + "_" + imgPart[4] + "_" + str(
                format(xi, "04")) + "_" + str(format(y1, "04")) + "_" + str(format(xi + 511, "04")) + "_" + str(
                format(y2, "04")) + "_" + imgPart[5]
            print(imf)
            cv2.imwrite(tPath + "\\" + imf, imgCrop)
