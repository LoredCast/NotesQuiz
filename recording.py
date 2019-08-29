import pyaudio
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
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "temp_output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Main loop
frames = []
print(stream.read(1024))
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #data = np.fromstring(stream.read(CHUNK), 'Int16')
    #frames.append(data)



yData = list(chain.from_iterable(frames))
print(stream.read(1024))


fig, ax = plt.subplots()
line, = ax.plot(yData)


def update(data):
    line.set_ydata(data)
    return line,


def data_gen():
    while True:
        data = np.fromstring(stream.read(CHUNK * int((RATE / CHUNK * RECORD_SECONDS))), 'Int16')
        yield data


ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()

stream.stop_stream()
stream.close()
p.terminate()
