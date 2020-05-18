# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:50:51 2020

@author: Remi
"""

import pickle
import numpy as np
import scipy as sy
import scipy.fftpack as syfp
import matplotlib.pyplot as plt
from kb_utils import SaveLoad as SL;
import math

array = SL('load', 'Data'); #Load datafile with Kb_utils

#Gets the desired column
x_axis = array['1'][0]['x_files']; 
y_axis = array['1'][0]['y_files'];
z_axis = array['1'][0]['z_files'];

#Calculates the pythagorean double to find the absolute vector of the system
absolute_array = math.sqrt(x_axis**2 + y_axis**2 + z_axis**2); #Needs the pythagorean absolute of the 3 axis arrays

#array = np.load("filnavn"); #Reads data from file
length = len(absolute_array);

#df = np.genfromtxt(fileName, dtype = float, delimiter = ',', names = True) #Can be used to read from file, defining delimiter for coloumns in the file

x = sy.linspace(0.00001, length*0.00001, num=length); #Creates time data for x axis based on array length

#Perform FFT on the absolute and find the frequency spectrum with consideration to time data for x-axis
FFT = sy.fftpack.fftn(absolute_array);
freq = syfp.fftfreq(absolute_array.size, d=(x[1]-x[0]));

#Plot the function
plt.subplot(211);
plt.plot(x, absolute_array);
plt.subplot(212);
plt.plot(freq, sy.log10(FFT), 'x');
plt.show();