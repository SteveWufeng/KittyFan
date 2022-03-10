import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
PI = np.pi

def read_image(img_file: str) -> list:
    img = cv2.imread(img_file)
    return img

def cartesian_to_polar(x, y) -> tuple:
    r = math.sqrt((x**2) + (y**2))  # find distance from center to 
    if x != 0:
        theta = np.arctan((abs(y)/abs(x)))       # find theta (note that this theta can not tell which quadrant it is in)
    else:
        theta = PI/2               # special case for x = 0 (solve can not divide by 0 error)
    if x <= 0 and y > 0:
        theta += PI/2              # add 90 degree if point is at quadrant 2
    elif x < 0 and y <= 0:
        theta += PI                # add 180 if at quadrant 3
    elif x >= 0 and y < 0:
        theta += 3*PI/2            # add 270 if at quadrant 4

    return r, math.degrees(theta)

def round_theta(theta):
    """and theta to nearest int"""
    # round theta
    return round(theta)

def round_point_five(r) -> int:
    # round to the nearest 0.5
    return round (r)

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
                r, deg = cartesian_to_polar(x_adjusted, y_adjusted)
                # make r round to nearest 0.5, and theta to the nearest int
                r, deg = round_point_five(r), round_theta(deg)
                if (r < 72 and ((r, deg) not in polar_img)):
                    # get pixel color data
                    if (x <= center_x and y < center_y) or (x >= center_x and y >= center_y):
                        pixel = cartesianImg[x][y]
                    else:
                        pixel = cartesianImg[y][x]
                    color = (pixel[2]/255, pixel[1]/255, pixel[0]/255)

                    # add to the dictionary
                    polar_img[(r, deg)] = color

    return polar_img

def plot_image(img: list) -> None:
    # initialize plot
    plt.axes(projection='polar')
    point_size = 20

    polar_img = generate_polar_dictionary(img)
    for deg in range (0, 361):
        for r in range (0, 36):
            if ((r, deg) in polar_img):
                colors = polar_img[(r, deg)]
                plt.scatter(math.radians(deg), r, color=colors, s=point_size, cmap='hsv', alpha=0.75)    
    # show the plot
    plt.show()
        
def main():
    # while True:
        # print(round_point_five(float(input("enter num: "))))
    img_file = 'images/color_test_pattern.jpg'
    img = read_image(img_file)
    plot_image(img)

if __name__ == '__main__':
    main()
