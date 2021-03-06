import time
from rpi_ws281x import *
import argparse
import cv2
import math
import numpy

# LED strip configuration:
LED_COUNT      = 72      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_FREQ_HZ = 400000
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, wait_ms=50) -> None:
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

def read_img_file(filename) -> list:
    """
    read image file and return a matrix of img data
    @param file name of the image
    @return a 3D list of the image list[row][col][R, G, B]
    """
    img = cv2.imread(filename)
    return img

def cartesian_to_polar(x, y) -> tuple:
    """
    convert cartesian cortinate to polar cordinate
    @param x x cordinate of the cartesian
    @param y y cordinate of the cartesian
    @return radius, degree
    """
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

    return r, math.degrees(theta)

def round_theta(deg):
    """
    round theta to nearest int
    @param original degree with decimal
    @return rounded degree
    """
    # round theta
    return round(deg)

def round_point_five(r) -> tuple:
    """
    round radius to nearest 0.5
    @param r radius
    @return rounded r to nearest 0.5
    """
    return round(r)

def generate_polar_dictionary (cartesianImg) -> dict:
    """
    convert cartesian cordinate to polar cordinate img
    @param cartesianImg cartesian list of the image
    @return dict dicionary of {(r, deg) : color}
    """
    polar_img = dict()
    max_x, max_y = len(cartesianImg[0])-1, len(cartesianImg)-1
    center_x, center_y = max_x//2, max_y//2
    
    for y in range(max_y):
        for x in range(max_x):
            x_adjusted = x - center_x
            y_adjusted = center_y - y

            # crop image(only circle)
            if (x_adjusted**2 + y_adjusted**2 <= max_x**2/4):
                r, deg = cartesian_to_polar(x_adjusted, y_adjusted)
                if (x <= max_x//2 and y <= max_y//2-1) or (x >= max_x//2 and y > max_y//2):
                    pixel = cartesianImg[x][y]
                else:
                    pixel = cartesianImg[y][x]
                color = Color(int(pixel[2]), int(pixel[1]), int(pixel[0]))
                # make r round to nearest 0.5, and degree to the nearest int
                r, deg = round_point_five(r), round_theta(deg)

                # add to the dictionary
                polar_img[(r, deg)] = color

    return polar_img


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip2 = Adafruit_NeoPixel(LED_COUNT, 13, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    strip2.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        img_file = 'images/line.jpg'
        img = read_img_file(img_file)
        polar_img = generate_polar_dictionary(img)
        while True:
            for deg in range (0, 361,3):
                for r in range (0, LED_COUNT):
                    deg2 = round_theta(deg+180)
                    if (deg2 > 360):
                        deg2 -= 360
                    if (r, deg) in polar_img:
                        strip.setPixelColor(r, polar_img[r, deg])
                    if (r, deg2) in polar_img:
                        strip2.setPixelColor(r, polar_img[r, deg2])
                strip.show()
                strip2.show()
        
    except KeyboardInterrupt:
        if not args.clear:
            color_wipe(strip, Color(0,0,0), 0)
            color_wipe(strip2, Color(0,0,0), 0)
