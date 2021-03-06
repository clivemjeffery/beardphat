#!/usr/bin/env python

import colorsys
import math
import signal
import time
from random import randint, sample
import argparse
import sys

if sys.platform == 'darwin':
  from mote import Mote
  motephat = Mote()
  motephat.configure_channel(1, 16, False)
  motephat.configure_channel(2, 16, False)
else:
  import motephat
  motephat.set_brightness(1)

parser = argparse.ArgumentParser()
parser.add_argument("sequence", choices=['sparkle', 'flash'], help="Type of mote sequence to play.")
parser.add_argument("-i", "--interval", default=0.1, type=float, help="Interval between sparkles in seconds (default=0.1).")
parser.add_argument("-d", "--density", default=8, type=int, help="Light between 1 and DENSITY pixels each interval (default=8, max=16).")
parser.add_argument("-r", "--red", default='255,255', help="Range of red colour values to be chosen from.")
parser.add_argument("-g", "--green", default='255,255', help="Range of green.")
parser.add_argument("-b", "--blue", default='255,255', help="Range of blue.")
parser.add_argument("-k", "--keepcolour", action="store_true", help="Keep chosen colour during interval.")
args = parser.parse_args()

# Validate arguments
def validate_colour_range(arg):
  colour_range = [0, 0]
  try:
    possible_list = arg.split(',')
    colour_range[0] = int(possible_list[0])
    colour_range[1] = int(possible_list[1])
    for colour in colour_range:
      if colour > 255:
        colour = 255
      if colour < 0:
        colour = 0
  except Exception: # just fail to white
    colour_range = [255,255]
  return colour_range

if args.density > 16:
  args.density = 16

reds = validate_colour_range(args.red)
greens = validate_colour_range(args.green)
blues = validate_colour_range(args.blue)

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

def randclr(colour_range):
  return randint(colour_range[0], colour_range[1])

def randomise_colours():
  r = randclr(reds)
  g = randclr(greens)
  b = randclr(blues)
  return [r, g, b]

def sparkle():
  while gsentinel.good:
    pix1s = sample(range(16),randint(0,args.density))
    pix2s = sample(range(16),randint(0,args.density))
    c = randomise_colours()
    for cpix in pix1s:
      if not args.keepcolour:
        c = randomise_colours()
      motephat.set_pixel(1, cpix, c[0], c[1], c[2])
      motephat.show()
    for cpix in pix2s:
      if not args.keepcolour:
        c = randomise_colours()
      motephat.set_pixel(2, cpix, c[0], c[1], c[2])
      motephat.show()
    time.sleep(args.interval)
    motephat.clear()

def flash():
  alt = 0 # toggle between 0 and 1 to alternate flashing pixels
  while gsentinel.good:
    pixlist = range(0+alt,16+alt,2)
    c = randomise_colours()
    for cpix in pixlist:
      if not args.keepcolour:
        c = randomise_colours()
      motephat.set_pixel(1, cpix, c[0], c[1], c[2])
      motephat.set_pixel(2, cpix, c[0], c[1], c[2])
    motephat.show()
    time.sleep(args.interval)
    motephat.clear()
    motephat.show()
    time.sleep(args.interval)
    if alt == 0:
      alt = 1
    else:
      alt = 0

def main():
  try:

    if args.sequence == 'sparkle':
      sparkle()
    if args.sequence == 'flash':
      flash()
    else:
      if gsentinel.good: # otherwise we've been interrupted in a sequence
        print('sequence %s not defined.' % args.sequence)

  finally:
    motephat.clear()
    motephat.show()
    time.sleep(0.1)

if __name__=="__main__":
  main()
