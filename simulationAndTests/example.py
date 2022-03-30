#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import random

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_FREQ_HZ = 400000
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

S = [
    [0, 1, 1, 1, 1, 0], 
    [1, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 0, 0], 
    [0, 0, 0, 0, 1, 0], 
    [0, 0, 0, 0, 1, 0], 
    [1, 1, 1, 1, 0, 0]
]
T = [
    [1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0]
]
E = [
    [1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0]
]
V = [
    [1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0]
]
def display_row(strip, a_list, on_color, off_color):
    colored = []
    for i in a_list:
        if i == 1:
            colored.append(on_color)
        elif i == 0:
            colored.append(off_color)
    index = 40
    for pixel in colored:
        strip.setPixelColor(index, pixel)
        index +=1
    strip.show()

def display_steve(strip, wait_ms=0.1):
    for i in range(5):
        row = []
        for letter in [S, T, E, V, E]:
            row += letter[i]
        display_row(strip, row, Color(0, 0, 100), Color(0, 0, 0))
    time.sleep(wait_ms/1000.0)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def random_index_color():
    r = 255
    g = 0
    b = 0
    return random.randint(0,5), r, g, b

def custom():
    led_index = int(input('led index #: '))
    r, g, b = 0, 0, 0
    color = input('Enter R G B: ')
    color = color.split()
    r, g, b = int(color[0]), int(color[1]), int(color[2])
    return led_index, r, g, b
    

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            display_steve(strip, 1000)
        
        
        # index, r, g, b = 0, 50, 0, 0
        # while True:
            
        #     for i in range(0,):
        #         strip.setPixelColor(index+i, Color(r,g,b))
        #     strip.show()
        #     if r:
        #         r = 0
        #         g = 50
        #     elif g:
        #         g = 0
        #         b = 50
        #     else:
        #         b = 0
        #         r = 50
            
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0),0)  # Red wipe
            #colorWipe(strip, Color(0, 255, 0),0)  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255),0)  # Green wipe
            # print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127),0)  # White theater chase
            #theaterChase(strip, Color(127,   0,   0),0)  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127),0)  # Blue theater chase
            # print ('Rainbow animations.')
            #rainbow(strip,0)
            #rainbowCycle(strip,0)
            #theaterChaseRainbow(strip, 0)
            #colorWipe(strip, Color(0,0,0), 10)
            # break
    except KeyboardInterrupt:
        if not args.clear:
            colorWipe(strip, Color(0,0,0), 0)