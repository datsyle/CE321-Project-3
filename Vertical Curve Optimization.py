# Project 3 Vertical Curve Design / Optimization based on minimal earthworks

import numpy as np

import math

import matplotlib.pyplot as plt

# for script's coordinate system: going uphill is positive grade, going downhill is negative grade, and all slope variages = G

horizontal_length = 2000 #ft

inital_elevation = 2100 #ft

final_elevation = 2050 #ft

resolution = 2000 # number of points taken along the horizontal axis

# option 1 is for a parabolic curve into a linear section into another parabolic curve

def SSD(design_speed, braking_friction, slope, PIJR = 2.5, gravitational_constant = 32.2):

    SSD = PIJR * design_speed + (design_speed**2) / (2 * gravitational_constant * (braking_friction - slope / 100))

    return SSD

def existing_elevation(horizontal_length, resolution, initial_elevation):

    x_range = np.arange(0, horizontal_length + horizontal_length / resolution, horizontal_length / resolution)

    y_range = np.array([])

    for x in x_range:

        y = 50 * math.cos(math.pi * x / horizontal_length) + initial_elevation

        y_range = np.append(y_range, y)

    return [x_range, y_range]

# function for a concave down vertical curve

def concave_down_vertical_curve(inital_height, first_station,  SSD, initial_slope, final_slope, second_station):
    
    A = final_slope - initial_slope

    # determine minimum horizontal length of starting vertical curve

    # SSD is less than curve length

    L_1 = (abs(A) * (SSD**2)) / 2158

    # SSD is greater than curve length

    L_2 = 2 * SSD - 2158 / abs(A)

    design_length = max([L_1, L_2])

    x_range = np.arange(first_station, round(first_station + design_length))

    # return x & y coordinates of curve

    y_range = np.array([])

    for x in x_range:

        y = (A / (200 * design_length)) * x**2 + (initial_slope / 100) * x + inital_height

        y_range = np.append(y_range, y)
  
    return [x_range, y_range]

# function for a concave up vertical curve

def concave_up_vertical_curve(final_height, first_station,  SSD, initial_slope, final_slope, second_station):

    
    A = final_slope - initial_slope

    # determine minimum horizontal length of starting vertical curve

    # SSD is less than curve length

    L_1 = (abs(A) * (SSD**2)) / 2158

    # SSD is greater than curve length

    L_2 = 2 * SSD - 2158 / abs(A)

    # SSD is less than curve length at night for concave up curve

    L_3 = (abs(A) * (SSD **2)) / (400 + 3.5 * SSD)

    # SSD is greater than curve length at night for concave up curve

    L_4 = 2 * SSD - (400 + 3.5 * SSD) / (abs(A))

    design_length = max([L_1, L_2, L_3, L_4])

    # return x & y coordinates of curve

    x_range = np.arange(round(-1 * design_length), 0)

    y_range = np.array([])

    for x in x_range:

        y = (A / (200 * design_length)) * x**2 + (initial_slope / 100) * x + final_height

        y_range = np.append(y_range, y)
  
    return [np.arange(round(second_station - design_length), second_station), y_range]

#example_concave_up = concave_up_vertical_curve(10, 0, 20, -10, 0, 200)

#print(example_concave_up)

existing_elevation = existing_elevation(horizontal_length, resolution, inital_elevation)

#plotting

x = existing_elevation[0]

y = existing_elevation[1]

plt.plot(x, y, linewidth=2.0)

plt.show()





