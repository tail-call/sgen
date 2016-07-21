#!/usr/bin/env python

# Run like this:
# $ python popcorn.py 44000 | aplay -r 44000

from sgen import *

SAMPLE_RATE = int(sys.argv[1])

sq1 = SquareOsc(amplitude=0.3, rate=SAMPLE_RATE)
m1 = melody([
             note("G5"), 0,
             note("F5"), 0,
             note("G5"), 0,
             note("D5"), 0,
             note("Bb4"), 0,
             note("D5"), 0,
             note("G4"), 0,
             0, 0,
             note("G5"), 0,
             note("F5"), 0,
             note("G5"), 0,
             note("D5"), 0,
             note("Bb4"), 0,
             note("D5"), 0,
             note("G4"), 0,
             0, 0,
             note("G5"), 0,
             note("A5"), 0,
             note("Bb5"), 0,
             note("A5"), 0,
             note("Bb5"), 0,
             note("G5"), 0,
             note("A5"), 0,
             note("G5"), 0,
             note("A5"), 0,
             note("F5"), 0,
             note("G5"), 0,
             note("D5"), 0,
             note("Bb4"), 0,
             note("D5"), 0,
             note("G5"), 0,
             0, 0,
            ])
sq2 = SawOsc(amplitude=0.2, rate=SAMPLE_RATE)
m2 = melody([
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("A#2"), 0,
             note("A#3"), 
             note("F3"),
             note("A#2"), 0,
             note("A#3"), 
             note("F3"),
             note("A2"), 0,
             note("A3"), 
             note("F3"),
             note("A2"), 0,
             note("A3"), 
             note("F3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
             note("G2"), 0,
             note("G3"), 
             note("D3"),
            ])

sq3 = NoiseOsc(amplitude=0.2, rate=SAMPLE_RATE)
m3 = melody([
             0, 0, note("G2"), 0,
             0, 0, note("G2"), 0,
            ])

ticks = 0
state = 18

while True:
    s1 = sq1.nextsample()
    s2 = sq2.nextsample()
    s3 = sq3.nextsample()

    writesample(s1+s2+s3)

    ticks = ticks + 1
    if ticks > SAMPLE_RATE/150: # 150 times per second
        ticks = 0
        state = state + 1
        sq1.amplitude = sq1.amplitude*0.7
        sq2.amplitude = sq2.amplitude*0.95
        sq3.amplitude = sq3.amplitude*0.8

    if state > 17:
        state = 0
        sq1.amplitude = 0.3
        sq1.frequency = next(m1)
        sq2.amplitude = 0.2
        sq2.frequency = next(m2)
        sq3.amplitude = 0.2
        sq3.frequency = next(m3)
