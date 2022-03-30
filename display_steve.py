import time
from rpi_ws281x import *
import random

# copied conficurations---
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

# variables to display each character of my name.
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
def colorWipe(strip, color, wait_ms=50):
    """
    Wipe color across display a pixel at a time.
    @param strip Adafruit_NeoPixel instance of an led strip
    @param color color to wipe out the led stip
    @param wait_ms delay for updating each led pixel
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def display_row(strip, a_list, on_color, off_color):
    """
    input a 1D list, and display on the LED strip
    @param Adafruit_NeoPixel instance of an led strip
    @param a_list a list of status of leds 1 = ON, 0 = OFF.
    @param on_color the color for a turned on status LED.
    @param off_color the color for a turned off status LED.
    """
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
    """
    display steve on the LED strip
    @param strip LED strip to display on
    @param wait_ms time delay for each frame.
    """
    for i in range(5):
        row = []
        for letter in [S, T, E, V, E]:
            row += letter[i]
        display_row(strip, row, Color(0, 0, 100), Color(0, 0, 0))
    time.sleep(wait_ms/1000.0)

def random_index_color():
    """
    helper function to randomize a tuple of color
    @return a random index 0 to 5 with static RGB
    """
    r = 255
    g = 0
    b = 0
    return random.randint(0,5), r, g, b

def custom():
    """
    Learning how to use this library...
    helper functions that read inputs
    read an index from input
    and read rgb from input
    @return index and RGB
    """
    led_index = int(input('led index #: '))
    r, g, b = 0, 0, 0
    color = input('Enter R G B: ')
    color = color.split()
    r, g, b = int(color[0]), int(color[1]), int(color[2])
    return led_index, r, g, b

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        while True:
            display_steve(strip, 1000)
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 0)