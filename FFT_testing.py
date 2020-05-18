# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:54:50 2020

@author: Remi
"""


import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
from kb_utils import SaveLoad as SL;

config_file = SL('load', 'Data'); #Load datafile with Kb_utils
print (config_file);
#x_files = config_file['1'][0]['x_files'] #EngineId, timestamp, Column name

array_sine = [];
sine_t = np.linspace(0, 0.001, 100);

for t in sine_t:
    array_sine.append(np.sin(t));

#plt.ylabel("Amplitude")
#plt.xlabel("Frequency [Hz]")
plt.plot(sine_t, array_sine)
plt.grid()
plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_xlabel("time", fontsize = 15)
# ax.set_ylabel("sine", fontsize = 15)
# ax.plot(sine_t, array_sine)
# fig.show()
# ax.show()

#data = pd.read('file',index_col=0)
#data.index = pd.to_datetime(data.index)
#data = data['file'].astype(float).values

#N = data.shape[0] #number of elements
#t = np.linspace(0, N * 3600, N) #converting hours to seconds
#s = data

#fft = np.fft.fft(s)
#fftfreq = np.fft.fftfreq(len(s))

#T = t[1] - t[0]

#f = np.linspace(0, 1 / T, N)
#plt.ylabel("Amplitude")
#plt.xlabel("Frequency [Hz]")
#plt.plot(fftfreq,fft)
#plt.show()

