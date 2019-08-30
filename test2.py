import pyaudio
import time
from itertools import chain
import wave
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.fftpack import fft

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
SIZE = RECORD_SECONDS * RATE

WAVE_OUTPUT_FILENAME = "temp_output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#print(np.frombuffer(stream.read(CHUNK), 'float32'))
#frames = []

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #data = np.frombuffer(stream.read(CHUNK), 'float32')
    #frames.append(data)

#yData = list(chain.from_iterable(frames))


# fig, ax = plt.subplots()
# part, = ax.plot(yData)
# ax.set_ylim([-1, 1])


#def update(data):
#    part.set_ydata(data)
 #   return part


#def data_gen():
#    while True:
#        data = np.frombuffer(stream.read(CHUNK * int((RATE / CHUNK * RECORD_SECONDS))), 'float32')
#        yield data
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = np.frombuffer(stream.read(CHUNK), 'float32')
    frames.append(data)


frames = list(chain.from_iterable(frames))

T = 1 / RATE
x = np.linspace(0.0, 1.0 / (2 * T), int(SIZE / 2))

yr = fft(frames)
y = 2/SIZE * np.abs(yr[0:np.int(SIZE/2)])


freqs = dict(zip(x, y))

#plt.plot(x,y)
#plt.show()


for f in freqs:
    if freqs.get(f) > 0.04:
        print(f)


# ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
# plt.show()


stream.stop_stream()
stream.close()
p.terminate()
