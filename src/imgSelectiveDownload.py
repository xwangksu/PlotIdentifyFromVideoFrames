'''
Created on Jan 16, 2021

@author: xuwang
'''
import pandas as pd
import argparse

# ------------------------------------------------------------------------
ap = argparse.ArgumentParser()
# ==============
ap.add_argument("-p", "--plotFile", required=True,
                help="plot start/end file")

# ==============
args = ap.parse_args()
plotMap = args.plotFile
dateTime = "20190519"
camSerial = "A06276"
finalFile = open("D:\\raw_download_20190519.txt",'w')
# ------------------------------------------------------------------------
dfPlot = pd.read_csv(plotMap, header=None)
for i in range(24):  # read ByPlot file, 28 folders, north-south
    col = "C" + str(format(i + 1, "03"))
    # print(col)
    folderName = "DJI_" + camSerial + "_" + col + "_" + dateTime
    for j in range(28):  # 28 rows, east to west
        if dfPlot[i][j * 2] < dfPlot[i][j * 2 + 1]:
            for fn in range(int(dfPlot[i][j * 2]), int(dfPlot[i][j * 2 + 1]) + 1):
                imgFileName = folderName + "_" + str(format(fn, "06")) + ".dng"
                finalFile.write("get ./"+folderName+"/"+imgFileName+"\n")
        else:  # great
            for fn in range(int(dfPlot[i][j * 2 + 1]), int(dfPlot[i][j * 2]) + 1):
                imgFileName = folderName + "_" + str(format(fn, "06")) + ".dng"
                finalFile.write("get ./" + folderName + "/" + imgFileName+"\n")
finalFile.close()





