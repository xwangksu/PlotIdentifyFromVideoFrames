'''
Created on Nov 5, 2019

@author: xuwang
'''
import pandas as pd
import os
import argparse
import cv2

#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
#==============
ap.add_argument("-p", "--plotFile", required=True,
    help="plot start/end file")
#==============
ap.add_argument("-m", "--mapFile", required=True,
    help="field map file")
#==============
ap.add_argument("-s", "--srcPath", required=True,
    help="source path")
#==============
ap.add_argument("-t", "--tgtPath", required=True,
    help="target path")
#==============
ap.add_argument("-b", "--baseline", required=True,
    help="ref position of height")
#==============
ap.add_argument("-sn", "--camsn", required=True,
    help="camera SN")
#==============
args = ap.parse_args()
sourcePath = args.srcPath
targetPath = args.tgtPath
plotMap = args.plotFile
fieldMap = args.mapFile
bp = args.baseline # 0.5
camSerial = args.camsn # A06276 
#------------------------------------------------------------------------
dfPlot = pd.read_csv(plotMap, header=None)
dfField = pd.read_csv(fieldMap, header=None)
plotMapFileFactors = plotMap.split("\\")
plotMapFile = plotMapFileFactors[len(plotMapFileFactors)-1]
dateCol = plotMapFile.split("_")[0]

for i in range(29): #read ByPlot file, 28 folders, north-south
    col = "C"+str(format(i+1,"03"))
    # print(col)
    folderName = "DJI_"+camSerial+"_"+col+"_"+str(dateCol)
#     print(sourcePath+"\\"+folderName)
    if os.path.exists(sourcePath+"\\"+folderName):
        for j in range(29): # 28 rows, east to west
            plotID = dfField[i][j]
            # print(plotID)
            if dfPlot[i][j*2] < dfPlot[i][j*2+1]:
                for fn in range(int(dfPlot[i][j*2]),int(dfPlot[i][j*2+1])+1):
                    imgFileName = sourcePath+"\\"+folderName+"\\TIFF\\"+folderName+"_"+str(format(fn,"06"))+".tif"
#                     imgFileName = sourcePath+"\\"+folderName+"\\TIFF\\"+"DJI_"+camSerial+"_"+"C"+str(format(i+4,"03"))+"_"+str(dateCol)+"_"+str(format(fn,"06"))+".tif"
                    # print(imgFileName)
                    if os.path.isfile(imgFileName):
                        imgFileProcessing = cv2.imread(imgFileName)
                        # Y - from center (base) +/- 256
                        y1 = int(imgFileProcessing.shape[0]*float(bp))-256
                        y2 = y1+512
                        # X 
                        x_min = int(imgFileProcessing.shape[1]/16)
                        x_max = int(imgFileProcessing.shape[1]/16*15)
                        for xi in range(x_min,x_max,512):
                            imgCrop = imgFileProcessing[y1:y2, xi:xi+512]
                            imf = folderName+"_"+str(format(fn,"06"))+"_"+str(format(xi,"04"))+"_"+str(format(y1,"04"))+"_"+str(format(xi+511,"04"))+"_"+str(format(y2,"04"))+"_"+plotID+".tif"
                            print(imf)
                            cv2.imwrite(targetPath+"\\"+imf, imgCrop)
            else: # great
                for fn in range(int(dfPlot[i][j*2+1]),int(dfPlot[i][j*2])+1):
                    imgFileName = sourcePath+"\\"+folderName+"\\TIFF\\"+folderName+"_"+str(format(fn,"06"))+".tif"
#                     imgFileName = sourcePath+"\\"+folderName+"\\TIFF\\"+"DJI_"+camSerial+"_"+"C"+str(format(i+4,"03"))+"_"+str(dateCol)+"_"+str(format(fn,"06"))+".tif"
                    # print(imgFileName)
                    if os.path.isfile(imgFileName):
                        imgFileProcessing = cv2.imread(imgFileName)
                        # Y - from center (base) +/- 256
                        y1 = int(imgFileProcessing.shape[0]*float(bp))-256
                        y2 = y1+512
                        # X 
                        x_min = int(imgFileProcessing.shape[1]/16)
                        x_max = int(imgFileProcessing.shape[1]/16*15)
                        for xi in range(x_min,x_max,512):
                            imgCrop = imgFileProcessing[y1:y2, xi:xi+512]
                            imf = folderName+"_"+str(format(fn,"06"))+"_"+str(format(xi,"04"))+"_"+str(format(y1,"04"))+"_"+str(format(xi+511,"04"))+"_"+str(format(y2,"04"))+"_"+plotID+".tif"
                            print(imf)
                            cv2.imwrite(targetPath+"\\"+imf, imgCrop)
    else:
        print("No folder found")    
        
    


