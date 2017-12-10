#!/usr/bin/env python

import colorsys
import math
import signal
import time
from random import randint, sample
import argparse

import motephat
motephat.set_brightness(1)

parser = argparse.ArgumentParser()
parser.add_argument("sequence", choices=['sparkle', 'flash'], help="Type of mote sequence to play.")
parser.add_argument("-i", "--interval", default=0.1, type=float, help="Interval between sparkles in seconds (default=0.1).")
parser.add_argument("-d", "--density", default=8, type=int, help="Light between 1 and DENSITY pixels each interval.")
parser.add_argument("-c", "--colourmin", default=255, type=int, help="Minimum colour value chosen at random.")
parser.add_argument("-m", "--colourmax", default=255, type=int, help="Maximum colour value chosen at random.")
parser.add_argument("-b", "--blockcolour", action="store_false", help="Block a single colour in each interval.")
args = parser.parse_args()
if args.density > 32:
  args.density =32
if args.colourmax > 255:
  args.colourmax = 255
if args.colourmin > args.colourmax:
  args.colourmin = args.colourmax
if args.interval > 2:
  args.interval = 2

class Sentinel:
  good = True
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.good = False

gsentinel = Sentinel()

def sparkle():
  while gsentinel.good:
    pixlist = sample(range(32),randint(1,args.density))
    r = randint(args.colourmin, args.colourmax)
    g = randint(args.colourmin, args.colourmax)
    b = randint(args.colourmin, args.colourmax)
    for cpix in pixlist:      
      if args.blockcolour:
        r = randint(args.colourmin, args.colourmax)
        g = randint(args.colourmin, args.colourmax)
        b = randint(args.colourmin, args.colourmax)
      if cpix < 16:
        motephat.set_pixel(1, cpix, r, g, b)
      else:
        motephat.set_pixel(2, cpix-16, r, g, b)
      motephat.show()
    time.sleep(args.interval)
    motephat.clear()

def main():
  try:

    if args.sequence == 'sparkle':
      sparkle()
    else:
      print('sequence %s not defined.' % args.sequence)

  finally:
    motephat.clear()
    motephat.show()
    time.sleep(0.1)    

if __name__=="__main__":
  main()