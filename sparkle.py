#!/usr/bin/env python

import colorsys
import math
import time
from random import randint

import motephat

motephat.set_brightness(1)

try:
    while True:
        cpix = randint(0,15)
        cchn = randint(1,2)
        br = randint(55,255)
        motephat.set_pixel(cchn, cpix, br, br, br)
        motephat.show()
	time.sleep(0.1)
        motephat.set_pixel(cchn, cpix, 0, 0, 0)
        motephat.show()

except KeyboardInterrupt:
    motephat.clear()
    motephat.show()
    time.sleep(0.1)
