'''
Created on Dec 18, 2017

@author: xuwang
'''
import rawpy
import imageio
import os
import argparse
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcPath", required=True,
    help="source image folder")
# ap.add_argument("-t", "--tgtPath", required=True,
#     help="target folder to save the maker list")
args = ap.parse_args()
srcImagePath = args.srcPath
# tgtImagePath = args.tgtPath
#------------------------------------------------------------------------
exten = 'dng'
imList=[]
for dirpath, dirnames, files in os.walk(srcImagePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the path: %d" % len(imList))
for img in imList:
    with rawpy.imread(img) as raw:
#        rgb = raw.postprocess(demosaic_algorithm=None, use_auto_wb=True, output_color = rawpy.ColorSpace.Adobe, half_size=True)
#        rgb = raw.postprocess(demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR, output_color=rawpy.ColorSpace.sRGB, use_camera_wb=True) # Linear, sRGB
        rgb = raw.postprocess(demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR, output_color=rawpy.ColorSpace.raw, use_camera_wb=True) # Linear, raw
        print(img)
        imageio.imsave(img.replace('.dng','.tif'), rgb)

        
