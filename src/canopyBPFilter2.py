'''
Created on May 14, 2018

@author: xuwang
'''
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, freqz
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import argparse
import csv
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
ampCanopy = df['Canopy_Rate_Index'].values.tolist() # -1 to 1
allCanopy = df['Canopy_Rate'].values.tolist() # percentage
imgFileNames = df
normAmp = [float(i)/max(allCanopy) for i in allCanopy]
#------------------------------------------------------------------------
Fs = 29.99 # Fs, sampling rate, frame rate, Frequency
Ts = 1.0/Fs # sampling interval
n = len(ampCanopy) # length of the signal(canopy cover)
T = n/Fs # total sampling period
t = np.arange(0, T, Ts) # time vector
# if len(t) != n:
#     t=np.arange(0,T+Ts,Ts)
#------------------------------------------------------------------------
# FFT
k = np.arange(n)
frq = k/T
frq = frq[range(int(n/2))]
Y = np.fft.fft(ampCanopy)/n
Y = Y[range(int(n/2))]
#------------------------------------------------------------------------
# Design Low-pass filter
order = 8
fs = Fs       # sample rate, Hz
cutoff = 1.3  # desired cutoff frequency of the filter, Hz, 1.6 1-AM3 2.4-IPSR
b, a = butter_lowpass(cutoff, fs, order)
#------------------------------------------------------------------------
# Filter the signal by applying the low-pass filter
y1 = butter_lowpass_filter(ampCanopy, cutoff, fs, order)
y2 = butter_lowpass_filter(normAmp, cutoff, fs, order)
#------------------------------------------------------------------------
# Find local peaks, y1
peaks_y1, _ = find_peaks(y1)
# peaks_y_sd = peaks_y.sort(reverse=True)
y1_peaks_sd = sorted(y1[peaks_y1], reverse=True)
if len(y1_peaks_sd)>=rn:
    height_peaks_th = y1_peaks_sd[rn-1]
    peaks_y1_rn, _ = find_peaks(y1, height=height_peaks_th)
else:
    peaks_y1_rn, _ = find_peaks(y1)
t1_peaks = peaks_y1_rn/Fs
#------------------------------------------------------------------------
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
#------------------------------------------------------------------------
#------------------------------------------------------------------------
fig, ax = plt.subplots(4,1)
# Plot original signal
print(len(t))
print(len(ampCanopy))
ax[0].plot(t,ampCanopy,'r-',linewidth=2)
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
plt.plot(t, y1, 'r-', linewidth=2, label='Filtered Index')
plt.plot(t, y2, 'b', linewidth=1, label='Filtered Rate')
plt.plot(t1_peaks, y1[peaks_y1_rn], 'gx')
plt.plot(t2_peaks, y2[peaks_y2_rn], 'kx')
plt.xlabel('Time [sec]')
plt.ylabel('CCover Indicator')
plt.grid()
plt.legend()
#------------------------------------------------------------------------
plt.subplots_adjust(hspace=1)
plt.savefig(args.srcPath+"\\Fig_process.png")
plt.show()
plt.close()
#========================================================================
# sourceFile = args.srcFile
# outputPath = args.targetPath
st_range=sourceFile.find("_C0")+3
rangeNum = int(sourceFile[st_range:st_range+2])
print("Range Number: %d" % rangeNum)
print("Peaks 1: ", peaks_y1_rn)
print("Peaks 2: ", peaks_y2_rn)
df2 = pd.read_csv(sourceFile, usecols=[0], dtype=str)
imgFileNames = df2['Image_file'].values.tolist() # image file nams
finalFile = open(args.srcPath+"\\peaks.csv",'wt')
try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    if len(peaks_y1_rn) == len(peaks_y2_rn):
        writer.writerow(('Column','Image_file','Image_file_1','Image_file_2','Canopy_Rate_Index','Canopy_Rate'))
        if (rangeNum % 2) == 0: # even ranges, go from north to south
            for i in range(len(peaks_y1_rn)):
                col = i+1
                imf1 = imgFileNames[peaks_y1_rn[i]]
                imf2 = imgFileNames[peaks_y2_rn[i]]
                imf = imgFileNames[int(0.5*(peaks_y1_rn[i]+peaks_y2_rn[i]))]
                plotRate = ampCanopy[peaks_y1_rn[i]]
                plotRateAll = ampCanopy[peaks_y1_rn[i]]
                #---------------------------------------------------
                writer.writerow((col, imf, imf1, imf2, plotRate, plotRateAll))
        else: # odd ranges, go from south to north, flip
            for i in range(len(peaks_y1_rn)):
                col = i+1
                imf1 = imgFileNames[peaks_y1_rn[rn-1-i]]
                imf2 = imgFileNames[peaks_y2_rn[rn-1-i]]
                imf = imgFileNames[int(0.5*(peaks_y1_rn[rn-1-i]+peaks_y2_rn[rn-1-i]))]
                plotRate = ampCanopy[peaks_y1_rn[rn-1-i]]
                plotRateAll = ampCanopy[peaks_y1_rn[rn-1-i]]
                #---------------------------------------------------
                writer.writerow((col, imf, imf1, imf2, plotRate, plotRateAll))
    else:
        writer.writerow(('Column','Image_file','Canopy_Rate_Index','Canopy_Rate'))
        if (rangeNum % 2) == 0: # even ranges, go from north to south
            for i in range(len(peaks_y2_rn)):
                col = i+1
                imf = imgFileNames[peaks_y2_rn[i]]
                plotRate = ampCanopy[peaks_y2_rn[i]]
                plotRateAll = ampCanopy[peaks_y2_rn[i]]
                #---------------------------------------------------
                writer.writerow((col, imf, plotRate, plotRateAll))
        else: # odd ranges, go from south to north, flip
            for i in range(len(peaks_y2_rn)):
                col = i+1
                imf = imgFileNames[peaks_y2_rn[len(peaks_y2_rn)-1-i]]
                plotRate = ampCanopy[peaks_y2_rn[len(peaks_y2_rn)-1-i]]
                plotRateAll = ampCanopy[peaks_y2_rn[len(peaks_y2_rn)-1-i]]
                #---------------------------------------------------
                writer.writerow((col, imf, plotRate, plotRateAll))
finally:
    finalFile.close()      
    