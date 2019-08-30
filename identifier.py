from numpy import *
import math
from matplotlib import pyplot as plt
from scipy.fftpack import fft

t_start = 0  # time in s
t_end = 1  # time in s
sampling_rate = 1024  # in Hz
N = (t_end - t_start)*sampling_rate  # number of samples in set interval

# frequencies in set interval

freq1_Hz = 100  # Hz
freq1_Mag = 40  # Magnitude of Freq

freq2_Hz = 300  # Hz
freq2_Mag = 20  # Magnitude of Freq

freq3_Hz = 250  # Hz
freq3_Mag = 10  # Magnitude of Freq


# Data

time = linspace(t_start, t_end, N)
y_data = freq1_Mag * sin(2*math.pi * freq1_Hz * time) + \
         freq2_Mag * sin(2*math.pi * freq2_Hz * time) + \
         freq3_Mag * sin(2*math.pi * freq3_Hz * time)

T = 1/sampling_rate  # inverse of the sampling rate
x = linspace(0.0, 1.0/(2.0*T), int(N/2))

y_fft = fft(y_data)
y = 2/N * abs(y_fft[0:int(N/2)])

plt.plot(x,y)
plt.show()



