'''
Created on May 26, 2020

@author: xuwang
'''

import pandas as pd
import numpy as np
from scipy.signal import butter
from scipy.signal import filtfilt
from scipy.signal import freqz
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import argparse
import csv
# import statistics as stat
#------------------------------------------------------------------------
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data, method = "gust")
    return y
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcPath", required=True,
    help="source folder with canopy rate file")
#==============
# ap.add_argument("-p", "--pltFile", required=True,
#     help="plot layout file")
#==============
# ap.add_argument("-t", "--targetPath", required=True,
#     help="output path")
#==============
args = ap.parse_args()
sourceFile = args.srcPath+"\\CanopyCoverRate.csv"
# outputPath = args.targetPath
# Number of ranges 2018AM3 28, 2018IPSR 51, 2017AYN 56
rn = 28
#------------------------------------------------------------------------
df = pd.read_csv(sourceFile, usecols=[1,2], dtype=float)
# ampCanopy = df['Canopy_Rate_Index'].values.tolist() # -1 to 1
df['Can_reverse1'] = 1 - df['Canopy_Rate1']
allCanopy = df['Can_reverse1'].values.tolist() # percentage
imgFileNames = df
normAmp = [float(i)/max(allCanopy) for i in allCanopy]

df['Can_reverse2'] = 1 - df['Canopy_Rate2']
allCanopy2 = df['Can_reverse2'].values.tolist() # percentage
imgFileNames = df
normAmp2 = [float(i)/max(allCanopy2) for i in allCanopy2]


#------------------------------------------------------------------------
Fs = 30 # Fs, sampling rate, frame rate, Frequency
Ts = 1.0/Fs # sampling interval
n = len(allCanopy) # length of the signal(canopy cover)
T = n/Fs # total sampling period
t = np.arange(0, T, Ts) # time vector
if len(t) != n:
    t = t[0:len(t)-1]
    
n2 = len(allCanopy2) # length of the signal(canopy cover)
T2 = n2/Fs # total sampling period
t2 = np.arange(0, T2, Ts) # time vector
if len(t2) != n2:
    t2 = t[0:len(t2)-1]
#------------------------------------------------------------------------
# FFT
k = np.arange(n)
frq = k/T
frq = frq[range(int(n/2))]
Y = np.fft.fft(allCanopy)/n
Y = Y[range(int(n/2))]


k2 = np.arange(n2)
frq2 = k2/T2
frq2 = frq2[range(int(n2/2))]
Y2 = np.fft.fft(allCanopy2)/n2
Y2 = Y[range(int(n2/2))]


#------------------------------------------------------------------------
# Design Low-pass filter
order = 8
fs = Fs       # sample rate, Hz
cutoff = 1.3  # desired cutoff frequency of the filter, Hz, 1.6 1-AM3 2.4-IPSR
b, a = butter_lowpass(cutoff, fs, order)
#------------------------------------------------------------------------
# Filter the signal by applying the low-pass filter
y2 = butter_lowpass_filter(normAmp, cutoff, fs, order)

y4 = butter_lowpass_filter(normAmp2, cutoff, fs, order)

# Find local peaks, y2
peaks_y2, _ = find_peaks(y2)
# peaks_y_sd = peaks_y.sort(reverse=True)
y2_peaks_sd = sorted(y2[peaks_y2], reverse=True)
if len(y2_peaks_sd)>=rn:
    height_peaks_th = y2_peaks_sd[rn-1]
    peaks_y2_rn, _ = find_peaks(y2, height=height_peaks_th)
else:
    peaks_y2_rn, _ = find_peaks(y2)
t2_peaks = peaks_y2_rn/Fs


peaks_y4, _ = find_peaks(y4)
# peaks_y_sd = peaks_y.sort(reverse=True)
y4_peaks_sd = sorted(y4[peaks_y4], reverse=True)
if len(y4_peaks_sd)>=rn:
    height_peaks_th2 = y4_peaks_sd[rn-1]
    peaks_y4_rn, _ = find_peaks(y4, height=height_peaks_th2)
else:
    peaks_y4_rn, _ = find_peaks(y4)
t4_peaks = peaks_y4_rn/Fs
#------------------------------------------------------------------------
#------------------------------------------------------------------------
fig, ax = plt.subplots(4,1)
# Plot original signal
print("Down Bound ", len(peaks_y2_rn))
print("Up Bound ", len(peaks_y4_rn))
print(len(t))
print(len(allCanopy))
# ax[0].plot(t,ampCanopy,'r-',linewidth=2)
ax[0].plot(t,normAmp,'b',linewidth=1)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('CCover Indicator')
ax[0].set_ylim(-2,2)
#------------------------------------------------------------------------
# Plot frequency domain
ax[1].plot(frq,abs(Y),'r')
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
#------------------------------------------------------------------------
# Plot frequency response of the low-pass filter
w, h = freqz(b, a, worN=2000)
plt.subplot(4, 1, 3)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Attenuation')
plt.grid()
#------------------------------------------------------------------------
# Plot filtered signal
plt.subplot(4, 1, 4)
# plt.plot(t, y1, 'r-', linewidth=2, label='Filtered Index')
plt.plot(t, y2, 'b', linewidth=1, label='Filtered Rate')
# plt.plot(t1_peaks, y1[peaks_y1_rn], 'gx')
plt.plot(t2_peaks, y2[peaks_y2_rn], 'kx')
plt.xlabel('Time [sec]')
plt.ylabel('CCover Indicator')
plt.grid()
plt.legend()
#------------------------------------------------------------------------
plt.subplots_adjust(hspace=1)
plt.show()
#========================================================================
# sourceFile = args.srcFile
# outputPath = args.targetPath
st_range=sourceFile.find("_C0")+3
rangeNum = int(sourceFile[st_range:st_range+2])
print("Range Number: %d" % rangeNum)
# print("Peaks: ", peaks_y1_rn)
df2 = pd.read_csv(sourceFile, usecols=[0], dtype=str)
# print("Green dots: ", peaks_y1_rn)
print("Black dots: ", peaks_y2_rn)
# # y1_list = peaks_y1_rn.tolist()
# y2_list = peaks_y2_rn.tolist()
# delta_y2 = []
# for j in range(len(y2_list)-1):
#     delta_y2.append(y2_list[j+1]-y2_list[j])
# sd_y2 = sorted(delta_y2, reverse=False)
# print(stat.median(sd_y2))

imgFileNames = df2['Image_file'].values.tolist() # image file nams
finalFile = open(args.srcPath+"\\peaks.csv",'wt')

try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    # writer.writerow(('Column','Image_file'))
    if (rangeNum % 2) == 1:
        for i in range(len(peaks_y4_rn)):
            col = i+1
            imf = imgFileNames[peaks_y4_rn[len(peaks_y4_rn)-1-i]]
            imgNum = imf.split("_")[4]
            imgNum = int(imgNum.split(".")[0])
            #---------------------------------------------------
            writer.writerow((col, imgNum)) 
        for i in range(len(peaks_y2_rn)):
            col = i+1
            imf = imgFileNames[peaks_y2_rn[len(peaks_y2_rn)-1-i]]
            imgNum = imf.split("_")[4]
            imgNum = int(imgNum.split(".")[0])
            #---------------------------------------------------
            writer.writerow((col, imgNum))
    else:
        for i in range(len(peaks_y4_rn)):
            col = i+1
            imf = imgFileNames[peaks_y4_rn[i]]
            imgNum = imf.split("_")[4]
            imgNum = int(imgNum.split(".")[0])
            #---------------------------------------------------
            writer.writerow((col, imgNum)) 
        for i in range(len(peaks_y2_rn)):
            col = i+1
            imf = imgFileNames[peaks_y2_rn[i]]
            imgNum = imf.split("_")[4]
            imgNum = int(imgNum.split(".")[0])
            #---------------------------------------------------
            writer.writerow((col, imgNum))
finally:
    finalFile.close()      
#     