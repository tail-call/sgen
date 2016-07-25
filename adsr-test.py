#!/usr/bin/env python

from sgen import *

SAMPLE_RATE = 44100

sq = Adsr(SquareOsc(amplitude=0.5, rate=SAMPLE_RATE),
          a_ms = 1, d_ms = 100, s_lv = 0.2, r_ms = 1000)

ctr = 0

while True:
    sm = sq.nextsample()

    writesample(sm)

    ctr += 1

    if ctr > 1 * SAMPLE_RATE: # 3 seconds later
        sq.stop()
