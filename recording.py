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
INTERVAL = 0.75  # in s
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


def gen_scale():

    pitches = [65.4064]
    root = 65.4064

    for Tone in range(47):
        root = root * 2 ** (1 / 12)
        pitches.append(round(root, 1))

    rootnotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    names = []

    for line in range(4):
        for e in rootnotes:
            if line > 0:
                names.append(e + str(line - 1))
            else:
                names.append(e)
    return pitches, names

class Notes:
    def __init__(self, pitches, notes):
        self.pitches = pitches
        self.notes = notes

    def find_closest(self, freq):
        closest = min(self.pitches, key=lambda x: abs(x - freq))
        Index = self.pitches.index(closest)

        return closest, self.notes[Index]


note = Notes(gen_scale()[0], gen_scale()[1])


def interval_fft():
    frames = []

    for i in range(0, int(RATE / CHUNK * INTERVAL)):  # loop through Interval by Chunk
        data = np.frombuffer(stream.read(CHUNK), 'float32')  # convert data from str to float
        frames.append(data)

    frames = list(chain.from_iterable(frames))  # flatten list
    yr = fft(frames)  # raw Fourier Transform
    y = 2 / SIZE * np.abs(yr[0:np.int(SIZE / 2)])  # only positive values

    return dict(zip(x, y))  # map freqs to amplitude


while True:
    freqs = interval_fft()
    loudestFreq = max(freqs, key=freqs.get)

    if loudestFreq > 20:
        print(round(max(freqs, key=freqs.get), 2))
    else:
        print("-")


# plt.plot(x,y)
# plt.show()


stream.stop_stream()
stream.close()
p.terminate()
