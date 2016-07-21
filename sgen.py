import sys

from math import floor
from random import random 

def clamp(x):
    """
    Converts a real number x ∈ [-1.0, + 1.0] to an unsigned 8 bit integer.
    """
    return floor((x+1.0)*128)


class Osc:
    """
    A generic oscillator class.
    """
    def __init__(self, frequency=440, amplitude=1.0, phase = 0,
                 rate=8000):
        self.rate = rate
        self.amplitude = amplitude
        self.phase = phase
        # Unfortunately I _have_ to keep this at the bottom because
        # frequency property depends on existence of `rate' variable.
        # Is there a way to work around this?
        self.frequency = frequency


    @property
    def frequency(self):
        return self._frequency


    @frequency.setter
    def frequency(self, value):
        self._frequency = value
        self.time_delta = self.frequency/self.rate


    def incphase(self):
        self.time_delta = self.frequency/self.rate
        self.phase = (self.phase + self.time_delta) % 1


    def nextsample(self):
        sample = self.amplitude * self.oscillate()
        self.incphase()
        return sample


    def oscillate(self):
        """
        A method to be defined in derived class.
        """
        pass


class SquareOsc(Osc):
    """
    Square wave oscillator.
    """
    def oscillate(self):
        if self.phase < 0.5:
            return 1.0
        else:
            return -1.0


class SawOsc(Osc):
    """
    Sawtooth wave oscillator.
    """
    def oscillate(self):
        return self.phase * 2 - 1

class NoiseOsc(Osc):
    """
    Noise generator.
    """
    def oscillate(self):
        if self.frequency > 0:
            return random()*2 - 1
        else:
            return 0


def writesample(x):
    sys.stdout.buffer.write(bytes([clamp(x)]))


def note(symbol):
    """
    For a given note symbol of form [abcdefg](#|b)?[0-9] returns this
    note's frequency.

    E.g. note("A4") == 440,
         note("C#3") == 138.59,
         note("Ab5") == 830.61.

    See <http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html> for details.
    """
    notes_offsets = { 'A': +0, 'B': +2, 'C': -9, 
                      'D': -7, 'E': -5, 'F': -4,
                      'G': -2 }
    base = 440 # frequency of A4 is 440 Hz
    root = 2**(1/12)

    offset = notes_offsets[symbol[0].upper()]

    symbol = symbol[1::]

    if symbol[0] == "#":
        offset += 1
        symbol = symbol[1::]

    if symbol[0] == "b":
        offset -= 1
        symbol = symbol[1::]

    multiplier = int(symbol[0])

    return base * root ** (offset - (4 - multiplier) * 12)


def melody(notes):
    i = 0

    while True:
        yield notes[i]
        i = (i+1) % len(notes)
