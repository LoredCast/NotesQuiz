import pyaudio
import time
from itertools import chain
import wave
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "temp_output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)










print(np.frombuffer(stream.read(CHUNK), 'Int16'))
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = np.frombuffer(stream.read(CHUNK), 'Int16')
    frames.append(data)




yData = list(chain.from_iterable(frames))


fig, ax = plt.subplots()
part, = ax.plot(yData)
ax.set_ylim([-100000, 100000])



def update(data):
    part.set_ydata(data)
    return part


def data_gen():
    while True:

        data = np.frombuffer(stream.read(CHUNK * int((RATE / CHUNK * RECORD_SECONDS))), 'Int16')
        yield data



ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()

stream.stop_stream()
stream.close()
p.terminate()
