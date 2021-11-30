'''
Created on Jan 16, 2021

@author: xuwang
'''
import os
import argparse
# ------------------------------------------------------------------------
ap = argparse.ArgumentParser()
# ==============
ap.add_argument("-p", "--tPath", required=True,
                help="plot start/end file")
# ==============
args = ap.parse_args()
tPath = args.tPath
srcImagePath = "/bulk/jpoland/images/X5R/processed/"+tPath
finalFile = open("/homes/xuwang/"+tPath+".txt",'w')
# ------------------------------------------------------------------------
exten = 'jpg'
imList = []
for dirpath, dirnames, files in os.walk(srcImagePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(name)
imList1 = []
for img in imList:
    imgPart = img.split("_")
    imList1.append(imgPart[0]+"_"+imgPart[1]+"_"+imgPart[2]+"_"+imgPart[3]+"_"+imgPart[4]+".jpg")
print("Total images in the path: %d" % len(imList1))
imList2 = []
for i in imList1:
    if i not in imList2:
        imList2.append(i)
print("Total unique images in the path: %d" % len(imList2))
for i in imList2:
    iPart = i.split("_")
    folderName = iPart[0]+"_"+iPart[1]+"_"+iPart[2]+"_"+iPart[3]
    finalFile.write("get ./" + folderName + "/" + i.replace(".jpg",".dng") + "\n")
finalFile.close()





