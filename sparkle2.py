#!/usr/bin/env python

import colorsys
import math
import time
from random import randint, sample

import motephat

motephat.set_brightness(1)

try:
  while True:
    pixlist = sample(xrange(16),randint(1,8))
    br = 255
    for cpix in pixlist:
      cchn = randint(1,2)
      motephat.set_pixel(cchn, cpix, br, br, br)
      motephat.show()
    time.sleep(0.1)
    motephat.clear()

except KeyboardInterrupt:
  motephat.clear()
  motephat.show()
  time.sleep(0.1)
