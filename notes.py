import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

PI = np.pi

def read_image(img_file: str) -> list:
    """
    img_file: path to input the image
    mode: 1 - for color image
          2 - for black and white 
    """
    img = cv2.imread(img_file)
    return img

    """imshow() method is for debuging, display the image"""
    # cv2.imshow('test', img)   # show the image preview.
    # cv2.waitKey(0)            # prompt the user to press any key, to prevent the windows from crashing
    # cv2.destroyAllWindows()   # close the window 

def cartesian_to_polar(x, y) -> tuple:
    r = math.sqrt((x**2) + (y**2))  # find distance from center to 
    if x != 0:
        theta = np.arctan((abs(y)/abs(x)))       # find theta (note that this theta can not tell which quadrant it is in)
    else:
        theta = PI/2                # special case for x = 0 (solve can not divide by 0 error)
    if x <= 0 and y > 0:
        theta += PI/2              # add 90 degree if point is at quadrant 2
    elif x < 0 and y <= 0:
        theta += PI                # add 180 if at quadrant 3
    elif x >= 0 and y < 0:
        theta += 3*PI/2            # add 270 if at quadrant 4

    return r, theta

def plot_image(img: list) -> None:
    """
    r: length
    theta: angle
    area: size of the plot
    colors: [R, G, B] -> list 
    """
    # initialize plot
    plt.axes(projection='polar')
    point_size = 50

    # plotting plots
    # calculate (x, y) cord to (r, theta) cord.
    max_x, max_y = len(img[0])-1, len(img)-1
    center_x, center_y = max_x//2, max_y//2

    for y in range(max_y):     # y -> [0, 1, 2, 3 ..., max_y-1]
        for x in range(max_x): # x -> [0, 1, 2, 3 ..., max_x-1]
            # convert cordinate
            # by default the cordinate center is at top left of the image
            # adjust cortinate center to the image center
            x_adjusted = x- center_x
            y_adjusted = center_y - y
            r, theta = cartesian_to_polar(x_adjusted, y_adjusted)

            # get pixel data
            pixel = img[y][x]
            blue, green, red = pixel[0]/255, pixel[1]/255, pixel[2]/255
            colors = [red, green, blue]

            # plot the point
            plt.scatter(theta, r, color=colors, s=point_size, cmap='hsv', alpha=0.75)
    
    # show the plot
    plt.show()

def main():
    img_file = 'favicon1.png'
    # plot_image('asd')
    img = read_image(img_file)
    plot_image(img)

if __name__ == '__main__':
    main()



"""
so in this case there is an easy and a more complete way to crop the image
first assume that your matrix is N x N, so it is the same number of rows and columns
then if you picture the following condition, it will tell you whether or not your (i,j) indexing is inside the circle: i**2 + j**2 <= N**2/4

why is it  **2/4 ?
because the radius of the circle is (N/2) so the radius squared is (N/2)^2=N^2/4

now if your matrix is actual N x M, you can just set the radius of your circle to r = min(N,M)/2
"""