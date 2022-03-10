import time
from rpi_ws281x import *
import argparse
import random
import cv2
import math
import numpy

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

# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def read_img_file(filename) -> list:
    """read image file and return a matrix of img data"""
    img = cv2.imread(filename)
    return img

def cartesian_to_polar(x, y) -> tuple:
    """convert cartesian cortinate to polar cordinate"""
    r = math.sqrt((x**2) + (y**2))
    if x != 0:
        theta = numpy.arctan((abs(y)/abs(x)))
    else:
        theta = numpy.pi/2
    if x <= 0 and y > 0:
        theta += numpy.pi/2
    elif x < 0 and y <= 0:
        theta += numpy.pi
    elif x >= 0 and y < 0:
        theta += 3*numpy.pi/2

    return r, theta

def round_point_five(r, theta) -> tuple:
    """round r to nearest 0.5 and theta to nearest int"""
    r_string = str(r).split(".")
    r_rounded = int(r_string[0])
    r_one_dec_place = int(r_string[1][0])
    if (r_one_dec_place > 3 and r_one_dec_place < 7):
        r_rounded += 0.5
    elif (r_one_dec_place >=7):
        r_rounded += 1
    return r_rounded, round(theta)

def generate_polar_dictionary (cartesianImg) -> dict:
    """convert cartesian cordinate to polar cordinate img"""
    polar_img = dict()
    max_x, max_y = len(cartesianImg[0])-1, len(cartesianImg)-1
    center_x, center_y = max_x//2, max_y//2
    
    for y in range(max_y):
        for x in range(max_x):
            x_adjusted = x - center_x
            y_adjusted = center_y - y

            # crop image(only circle)
            if (x_adjusted**2 + y_adjusted**2 <= max_x**2/4):
                r, theta = cartesian_to_polar(x_adjusted, y_adjusted)
            else:
                continue

            # get pixel color data
            if (x <= max_x//2 and y <= max_y//2-1) or (x >= max_x//2 and y > max_y//2):
                pixel = cartesianImg[x][y]
            else:
                pixel = cartesianImg[y][x]
            color = Color(pixel[2], pixel[1], pixel[0])

            # make r round to nearest 0.5, and theta to the nearest int
            r, theta = round_point_five(r, theta)

            # add to the dictionary
            polar_img[(r, theta)] = color

    return polar_img


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
            #TODO: set color
            print("placeholder")
    except KeyboardInterrupt:
        if not args.clear:
            colorWipe(strip, Color(0,0,0), 0)
