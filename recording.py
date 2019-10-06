import pyaudio
from random import *
import sys
import time
from itertools import chain
import numpy as np
from scipy.fftpack import fft

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
INTERVAL = 0.75  # in s
SIZE = INTERVAL * RATE
T = 1 / RATE
SPACE = np.linspace(0.0, 1.0 / (2 * T), int(SIZE / 2))
SENSITIVITY = 0.003  # which amplitudes get evaluated

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def gen_scale():
    pitches = [65.4064]
    root = 65.4064

    for Tone in range(55):
        root = root * 2 ** (1 / 12)
        pitches.append(round(root, 1))

    rootnotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    names = []

    for line in range(5):
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
        closest        = min(self.pitches, key=lambda x: abs(x - freq))
        index = self.pitches.index(closest)

        return closest, self.notes[index]


note = Notes(gen_scale()[0], gen_scale()[1])


def interval_fft():
    frames = []

    for i in range(0, int(RATE / CHUNK * INTERVAL)):  # loop through Interval by Chunk
        data = np.frombuffer(stream.read(CHUNK), 'float32')  # convert data from str to float
        frames.append(data)

    frames = list(chain.from_iterable(frames))  # flatten list
    yr = fft(frames)  # raw Fourier Transform
    y = 2 / SIZE * np.abs(yr[0:np.int(SIZE / 2)])  # only positive values

    return dict(zip(y, SPACE))  # map freqs to amplitude


def picknote():
    rand_pitch = note.pitches[randint(0, len(note.pitches))]
    rand_note = note.find_closest(rand_pitch)
    return rand_pitch, rand_note


def listen():
    fftvals = interval_fft()
    loudestfreq = 0
    maxamp = max(fftvals)
    if maxamp > SENSITIVITY:
        loudestfreq = fftvals[maxamp]

    if loudestfreq > 25:
        freq = round(loudestfreq, 2)
        n = note.find_closest(freq)

        return freq
    else:
        return 0


def quiz():
    while True:
        playednote = ""
        notepick = picknote()
        print("Play " + str(notepick[1][1]) + " @ " + str(notepick[1][0]) + "Hz")
        while playednote != notepick[1][1]:
            rawlisten = listen()
            playednote = note.find_closest(rawlisten)[1]
            # print(playednote, end="\r")
            if rawlisten > 25:
                sys.stdout.write('\r' + "You most likely played: " + playednote + " @ " + str(rawlisten) + "Hz")
            else:
                sys.stdout.write('\r' + "You most likely played: nothing")
        print("\nGood, now next one\n------------------")


if __name__ == "__main__":
    quiz()
