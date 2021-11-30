'''
Created on Jun 4, 2018

@author: Xu
'''
import pandas as pd
import os
import argparse
import cv2
import errno
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mapFile", required=True,
    help="field layout map file")
#==============
ap.add_argument("-s", "--srcPath", required=True,
    help="source path")
#==============
ap.add_argument("-b", "--baseline", required=True,
    help="source path")
#==============
args = ap.parse_args()
sourcePath = args.srcPath
plotMap = args.mapFile
bp = args.baseline
# Number of ranges 2018AM3 28, 2018IPSR 51, 2017AYN 56
# rn = 28
#------------------------------------------------------------------------
df = pd.read_csv(plotMap, usecols=[1,2], dtype=int)
rangeNum = df['harvest_range'].values.tolist() # range list of all
columnNum = df['harvest_column'].values.tolist() # column list of all
#------------------------------------------------------------------------
df2 = pd.read_csv(plotMap, usecols=[0], dtype=str)
plotIDs = df2['plot_id'].values.tolist() # plot ID of all
#------------------------------------------------------------------------
df3 = pd.read_csv(sourcePath+"\\peaks.csv", usecols=[0], dtype=int)
pColumns = df3['Column'].values.tolist() # column numbers in a range
#------------------------------------------------------------------------
df4 = pd.read_csv(sourcePath+"\\peaks.csv", usecols=[1], dtype=str)
pImages = df4['Image_file'].values.tolist() # peak image files in a range
#------------------------------------------------------------------------
# Get range
st_range=sourcePath.find("_C0")+3
rangeCurrent = int(sourcePath[st_range:st_range+2])
print("Range Number: %d" % rangeCurrent)

for i in range(len(pColumns)):
    # Match plot ID
    for rci in range(len(rangeNum)):
        if rangeCurrent==rangeNum[rci] and pColumns[i]==columnNum[rci]:
            plotIDCurrent = plotIDs[rci]
            break
    print("Plot ID: %s" % plotIDCurrent)
    # Get peak image number
    st_Num = int(pImages[i].find(".jpg"))-6
    peakImageNum = int(pImages[i][st_Num:st_Num+6])
    # Generate file name
    fileNamePieces = pImages[i].split('_')
    fileNamePrefix = fileNamePieces[0]+"_"+fileNamePieces[1]+"_"+fileNamePieces[2]+"_"+fileNamePieces[3]+"_"
    # Fill 6 digits, generate image list
    targetImageList = []
    for fi in range(peakImageNum-5,peakImageNum+6):
        targetImageList.append(fileNamePrefix+format(fi,"06")+".jpg")
    # Get coordinates of the crop images
    peakImageFile = cv2.imread(sourcePath+"\\"+pImages[i])
    # Y - from center (base) +/- 256
    y1 = int(peakImageFile.shape[0]*float(bp))-256
    y2 = y1+512
    # X 
    x_min = int(peakImageFile.shape[1]/16)
    x_max = int(peakImageFile.shape[1]/16*15)
    # Crop and save
    # Create renamed path
    try:
        os.makedirs(sourcePath+"\\crop")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    for imgFile in targetImageList:
        if os.path.isfile(sourcePath+"\\"+imgFile):
            imgFileProcessing = cv2.imread(sourcePath+"\\"+imgFile)
            for xi in range(x_min,x_max,512):
                imgCrop = imgFileProcessing[y1:y2, xi:xi+512]
                imf = imgFile.replace(".jpg","_")+str(format(xi,"04"))+"_"+str(format(y1,"04"))+"_"+str(format(xi+511,"04"))+"_"+str(format(y2,"04"))+"_"+plotIDCurrent+".jpg"
                print(imf)
                cv2.imwrite(sourcePath+"\\crop\\"+imf, imgCrop)
    
    



