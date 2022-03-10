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

    # make r round to nearest 0.5, and theta to the nearest int
    r, theta = round_point_five(r, theta)

    return r, theta

def round_point_five(r, theta) -> tuple:
    """round r to nearest 0.5 and theta to nearest int"""
    # round r
    r_string = str(r).split(".")
    r_rounded = int(r_string[0])
    r_one_dec_place = int(r_string[1][0])
    if (r_one_dec_place > 3 and r_one_dec_place < 7):
        r_rounded += 0.5
    elif (r_one_dec_place >=7):
        r_rounded += 1
        
    # round theta
    degree = math.degrees(theta)
    degree = round(degree) # round to nearest degree
    theta = math.radians(degree)
    
    return r_rounded, theta

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
                if (r < 72 and ((r, theta) not in polar_img)):
                    # get pixel color data
                    if (x <= center_x and y < center_y) or (x >= center_x and y >= center_y):
                        pixel = cartesianImg[x][y]
                    else:
                        pixel = cartesianImg[y][x]
                    color = (pixel[2]/255, pixel[1]/255, pixel[0]/255)

                    # add to the dictionary
                    polar_img[(r, theta)] = color

    return polar_img

def plot_image(img: list) -> None:
    # initialize plot
    plt.axes(projection='polar')
    point_size = 20

    polar_img = generate_polar_dictionary(img)
    for deg in range(0, 361):
        for r in range(0, 36):
            theta = math.radians(deg)
            if ((r, theta) in polar_img):
                colors = polar_img[(r, theta)]
                plt.scatter(theta, r, color=colors, s=point_size, cmap='hsv', alpha=0.75)
                if (r < 36 and ((r+0.5, theta+math.pi % (2*math.pi)) in polar_img)):
                    colors_ = polar_img[(r+0.5, theta+math.pi % (2*math.pi))]
                    plt.scatter(theta, r+0.5, color=colors_, s=point_size, cmap='hsv', alpha=0.75)
                
    
    # for key in polar_img:
    #     r, theta = key[0], key[1]
    #     colors = polar_img[(r, theta)]
    #     plt.scatter(theta, r, color=colors, s=point_size, cmap='hsv', alpha=0.75)
        
    
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
