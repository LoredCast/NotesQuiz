import pyaudio
import time
from itertools import chain
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.fftpack import fft

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
INTERVAL = 0.5  # in s
MIN = 0.1  # Sensitivity
SIZE = INTERVAL * RATE

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

T = 1 / RATE
x = np.linspace(0.0, 1.0 / (2 * T), int(SIZE / 2))

time = 0

Pitches = [65.4064]
Root = 65.4064
for Tone in range(48):
    Root = Root * 2 ** (1 / 12)
    Pitches.append(Root)

rootNotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
Notes = []
for line in range(4):
    for e in rootNotes:
        if line > 0:
            Notes.append(e + str(line-1))
        else:
            Notes.append(e)


Tones = dict(zip(Notes, Pitches))

print(Tones)


while True:
    frames = []

    for i in range(0, int(RATE / CHUNK * INTERVAL)):
        data = np.frombuffer(stream.read(CHUNK), 'float32')
        frames.append(data)

    frames = list(chain.from_iterable(frames))
    yr = fft(frames)
    y = 2 / SIZE * np.abs(yr[0:np.int(SIZE / 2)])

    freqs = dict(zip(x, y))
    time += INTERVAL

    for f in freqs:
        if freqs.get(f) > MIN:
            print(f)
    print(time)

# plt.plot(x,y)
# plt.show()


stream.stop_stream()
stream.close()
p.terminate()
