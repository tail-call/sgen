#!/usr/bin/env python

from sgen import *

tr = Tracker(instrument=Adsr(osc=SquareOsc(amplitude=0.3, inclination=0.25,
                                           rate=44100),
                             a_ms=100, d_ms=1000, s_lv=0.1, r_ms=1000),
             pattern="""
D4 - - - F4 - D4 - E4 - F4 G4 F4 - - E4 D4 - - - D4 E4 F4 G4 A4 - G4 A4 C5 - D5 C5
F4 - Bb4 - A4 - - - - - - -
D5 E5 F5 G5 A5 - G5 F5 E5 - F5 G5 F5 E5 D5 - F5 E5 D5 C#5 D5 E5 F5 G5 A#5 - A5 -
G5 - F5 - G5 - - - - - A5 - G5 - F5 - D5 - - - - - - -
             """, bpm=400)
fx = SineOsc(amplitude=0.2, frequency=1)

while True:
    writesample(tr.nextsample())
    tr.instrument.osc.inclination = 0.5 + fx.nextsample()
