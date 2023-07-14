#!/usr/bin/env python

from sgen import *

SAMPLE_RATE = 44100

sq = Adsr(SquareOsc(amplitude=0.5, rate=SAMPLE_RATE, frequency=880),
          a_ms = 1000, d_ms = 1000, s_lv = 0.2, r_ms = 1000)
mod = SineOsc(amplitude=0.1, rate=SAMPLE_RATE, frequency=4.8)

ctr = 0

while True:
    sm = sq.nextsample()
    sq.osc.frequency += mod.nextsample()

    writesample(sm)

    ctr += 1
    
    sq.osc.frequency -= 0.008

    if ctr > 1 * SAMPLE_RATE: # 1 second later
        sq.stop()
