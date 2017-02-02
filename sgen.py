import sys
    
from math import floor, pi, sin
from random import random 

DEFAULT_SAMPLE_RATE = 44100

def clamp(x):
    """
    Converts a real number x ∈ [-1.0, + 1.0] to an unsigned 8 bit integer.
    """
    if x >  1.0: x =  1.0
    if x < -1.0: x = -1.0
    return floor((x+1.0)*128)


def lookup(dictionary, key, safeguard=None):
    """
    Looks up for item in dictionary. Returns safeguard if item not found.
    """
    if key in dictionary:
        return dictionary[key]
    else:
        return safeguard


class Generator:
    """
    A generic generator class.
    """
    def __init__(self, **args):
        self.rate = lookup(args, 'rate', DEFAULT_SAMPLE_RATE)


    def nextsample(self):
        raise NotImplementedError


    def stop(self):
        pass
        #raise NotImplementedError


    def reset(self):
        pass
        #raise NotImplementedError


class Osc(Generator):
    """
    A generic oscillator class.
    """
    def __init__(self, **args):

        super().__init__(**args)
        self.amplitude = lookup(args, 'amplitude', 1.0)
        self.phase = lookup(args, 'phase', 0)

        self.frequency = lookup(args, 'frequency', 440)

        # A generic variabe for things like pulse width and whatnot
        self.inclination = lookup(args, 'inclination', 0.5)


    def incphase(self):
        phase_delta = self.frequency/self.rate
        self.phase = (self.phase + phase_delta) % 1


    def nextsample(self):
        sample = self.amplitude * self.oscillate()
        self.incphase()
        return sample


    def oscillate(self):
        raise NotImplementedError


class SquareOsc(Osc):
    """
    Square wave oscillator. _|¯|_|¯
    """
    def oscillate(self):
        if self.phase < self.inclination:
            return 1.0
        else:
            return -1.0


class SawOsc(Osc):
    """
    Sawtooth wave oscillator. /|/|/|/|
    """
    def oscillate(self):
        return self.phase * 2 - 1


class TriangleOsc(Osc):
    """
    Triangle wave oscillator. \/\/\/
    """
    def oscillate(self):
        if self.phase < (self.inclination % 1):
            return self.phase * 4 - 2
        else:
            return 2 - (self.phase) * 4


class SineOsc(Osc):
    """
    Sine wave oscillator.
    """
    def oscillate(self):
        return sin(self.phase * pi * 2)


class NoiseOsc(Osc):
    """
    Noise generator.
    """
    def oscillate(self):
        if self.frequency > 0:
            return random()*2 - 1
        else:
            return 0


class Adsr(Generator):
    """
    Attack-Decay-Sustain-Release wrapper for Osc objects.
    """
    def __init__(self, osc, a_ms, d_ms, s_lv, r_ms):

        assert(isinstance(osc, Osc))

        self.osc = osc
        self.attack = a_ms * 1e-3
        self.decay = d_ms * 1e-3
        self.sustain = s_lv
        self.release = r_ms * 1e-3

        # FIXME: BAD HACK
        self.rate = osc.rate

        self.reset()


    @property
    def frequency(self):
        return self.osc.frequency


    @frequency.setter
    def frequency(self, value):
        self.osc.frequency = value


    def nextsample(self):

        time_delta = 1/self.osc.rate

        def handle_attack(self):
            self.amplitude += time_delta/self.attack

            if self.amplitude >= 1.0:
                self.amplitude = 1.0
                self.state = 'decay'

        def handle_decay(self):
            self.amplitude -= time_delta / \
                              (self.decay * (1 - self.sustain))

            if self.amplitude <= self.sustain:
                self.amplitude = self.sustain
                self.state = 'hold'

        def handle_hold(self):
            """
            While you hold a note, amplitude won't change.
            """
            pass

        def handle_release(self):
            self.amplitude -= time_delta / \
                              (self.release / self.sustain)

            if self.amplitude <= 0:
                self.amplitude = 0
                self.state = 'hold'

        # Here comes the smart part.

        { 'attack' : handle_attack,
          'decay'  : handle_decay,
          'hold'   : handle_hold,
          'release': handle_release }[self.state](self)

        return self.amplitude * self.osc.nextsample()


    def stop(self):
        self.state = 'release'


    def reset(self):
        self.amplitude = 0.0
        self.state = 'attack'


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


class Tracker(Generator):
    """
    A generator that sequentially plays notes from pattern. 
    """

    def __init__(self, **args):
        super().__init__(**args)
        self.instrument = args['instrument']
        self.track = self.parse(args['pattern'])
        self.bpm = lookup(args, 'bpm', 150)
        self.period = self.instrument.rate/(self.bpm/60)
        self.counter = self.period


    def nextsample(self):
        self.counter += 1

        if self.counter > self.period:
            self.counter = 0
            next(self.track)

        return self.instrument.nextsample()

        

    def parse(self, pattern):
        for block in pattern.split():
            if block == "-":
                pass
            elif block == "!":
                self.instrument.stop()
            else:
                self.instrument.frequency = note(block)
                self.instrument.reset()
            yield
        self.reset()


def melody(notes):
    i = 0

    while True:
        yield notes[i]
        i = (i+1) % len(notes)
