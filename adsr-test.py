#!/usr/bin/env python

from sgen import *

SAMPLE_RATE = 44100

sq = Adsr(SineOsc(amplitude=0.5, rate=SAMPLE_RATE, frequency=220),
          a_ms = 100, d_ms = 1000, s_lv = 0.2, r_ms = 1000)
mod = SineOsc(amplitude=0.1, rate=SAMPLE_RATE, frequency=10)

ctr = 0

while True:
    sm = sq.nextsample()
    sq.osc.frequency += mod.nextsample()

    writesample(sm)

    ctr += 1

    if ctr > 1 * SAMPLE_RATE: # 3 seconds later
        sq.stop()
