#!/usr/bin/env python

from sgen import *

tr = Tracker(instrument=Adsr(osc=SquareOsc(amplitude=0.3, inclination=0.25,
                                           rate=44100),
                             a_ms=10, d_ms=300, s_lv=0.1, r_ms=1000),
             pattern="""
C4 - G#4 - G#4 - G#4 - G#4 - G4 - G4 - G4 - G4 - F4 - F4 - F4 - F4 - Eb4 - - - -  -
C4 - G#4 - G#4 - G#4 - G#4 - G4 - G4 - G4 - - C4 Bb4 - Bb4 - Bb4 - Bb4 - Ab4 - - - -  -
C4 - G#4 - G#4 - G#4 - G#4 - Bb4 - Bb4 - Bb4 - Bb4 - B4 - B4 - B4 - B4 - C5 - - - -  -
F4 - C5 - C5 - C5 - C5 - C#5 - C#5 - C#5 - C#5 - D5 - D5 - D5 - D5 - Eb5 - - - - - - -
C5 Eb5 - C5 Bb4 - Ab4 - F4 - Ab4 - Bb4 - Ab4 -
C5 Eb5 - C5 Bb4 - Ab4 - F4 - Ab4 - Ab4 - - -
C5 Eb5 - C5 Bb4 - Ab4 - F4 - Ab4 - Bb4 - Ab4 -
C5 C5 - Eb5 C5 Bb4 Ab4 - Ab4 - - - - - -


             """, bpm=500)

bass = Tracker(instrument=TriangleOsc(amplitude=0.3, inclination=0.4),
               pattern="""
C0 ! F3 ! C4 ! G#3 ! C4 ! F3 ! Db4 ! A#3 ! Db4 ! Eb3 ! Bb3 ! G3 ! Bb3 ! Ab3 ! Eb4 ! C4 ! Eb4 !
     F3 ! C4 ! G#3 ! C4 ! F3 ! Db4 ! A#3 ! Db4 ! Eb3 ! Bb3 ! G3 ! Bb3 ! Ab3 ! Eb4 ! C4 ! Eb4 !
     F3 ! C4 ! G#3 ! D3 ! G3 ! F3  ! G3  ! Db4 ! Eb3 ! Bb3 ! G3 ! Bb3 ! Ab3 ! Eb4 ! C4 ! Eb4 !
     F3 ! C4 ! G#3 ! D3 ! G3 ! F3  ! G3  ! Db4 ! Eb3 ! Bb3 ! G3 ! Bb3 ! Ab3 ! Eb4 ! C4 ! Eb4 !
Eb3 - - - E3 - - - F3 - - - E3 - - -
Eb3 - - - E3 - - - C3 - - - - - - -
Eb3 - - - E3 - - - F3 - - - E3 - - -
G3 - - - F3 - - - Eb3 - - - - - - -
               """, bpm=500)
fx = SineOsc(amplitude=0.2, frequency=1)

while True:
    writesample(tr.nextsample()+bass.nextsample())
    tr.instrument.osc.inclination = 0.5 + fx.nextsample()
