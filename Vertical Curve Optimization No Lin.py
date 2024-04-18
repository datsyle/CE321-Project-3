# Project 3 Vertical Curve Design / Optimization based on minimal earthworks

import numpy as np

import math

import matplotlib.pyplot as plt

# for script's coordinate system: going uphill is positive grade, going downhill is negative grade, and all slope variages = G

horizontal_length = 2000 #ft

initial_elevation = 2050 #ft

final_elevation = 2000 #ft

resolution = 2000 # number of points taken along the horizontal axis

# option 1 is for a parabolic curve into a linear section into another parabolic curve

def SSD(design_speed, slope, PIJR = 2.5, gravitational_constant = 32.2, braking_friction = 0.34):

    SSD = PIJR * design_speed + (design_speed**2) / (2 * gravitational_constant * (braking_friction - slope / 100))

    return SSD

def existing_elevation(horizontal_length, resolution, initial_elevation):

    x_range = np.arange(0, horizontal_length, horizontal_length / resolution)

    y_range = np.array([])

    for x in x_range:

        y = 50 * math.cos(math.pi * x / horizontal_length) + initial_elevation

        y_range = np.append(y_range, y)

    return [x_range, y_range]

# function for a concave down vertical curve

def design_length(initial_slope, final_slope, SSD, concavity):

    A = final_slope - initial_slope

    # SSD is less than curve length

    L_1 = (abs(A) * (SSD**2)) / 2158

    # SSD is greater than curve length

    L_2 = 2 * SSD - 2158 / abs(A)

    # SSD is less than curve length at night for concave up curve

    L_3 = (abs(A) * (SSD **2)) / (400 + 3.5 * SSD)

    # SSD is greater than curve length at night for concave up curve

    L_4 = 2 * SSD - (400 + 3.5 * SSD) / (abs(A))

    if concavity == "down":

        design_length = max([L_1, L_2])

    elif concavity == "up":

        design_length = max([L_1, L_2, L_3, L_4])

    if design_length > 2000:

        design_length = "too large"

    else:

        design_length = int(design_length)

    return design_length

def concave_down_vertical_curve(initial_height, first_station, initial_slope, final_slope, second_station, design_length):

    A = final_slope - initial_slope

    x_range = np.arange(first_station, round(first_station + design_length))

    # return x & y coordinates of curve

    y_range = np.array([])

    for x in x_range:

        y = (A / (200 * design_length)) * x**2 + (initial_slope / 100) * x + initial_height

        y_range = np.append(y_range, y)
  
    return [x_range, y_range]

# function for a concave up vertical curve

def concave_up_vertical_curve(final_height, first_station, initial_slope, final_slope, second_station, design_length):

    A = final_slope - initial_slope

    # return x & y coordinates of curve

    x_range = np.arange(round(-1 * design_length), 0)

    y_range = np.array([])

    for x in x_range:

        y = (A / (200 * design_length)) * x**2 + (final_slope / 100) * x + final_height

        y_range = np.append(y_range, y)
  
    return [np.arange(round(second_station - design_length), second_station), y_range]

def linear_downgrade(initial_height, first_station, final_height, second_station):

    slope = (final_height - initial_height) / (second_station - first_station)

    x_range = np.arange(first_station, second_station)

    y_range = np.array([])

    for x in x_range:

        y = slope * (x) + initial_height

        y_range = np.append(y_range, y)

    return [x_range, y_range]

def cut_and_fill_case2(first_vertical_curve, linear_section, second_vertical_curve, existing_elevation):

    range_of_analysis = np.array([])

    range_of_analysis = np.append(first_vertical_curve[1], [linear_section[1], second_vertical_curve[1]])

    return range_of_analysis - existing_elevation

def cut_and_fill_case1(total_vertical_curve, existing_elevation):

    cuts_or_fills = total_vertical_curve - existing_elevation

    # bad code -> can probably write into one for loop

    y_fill = [y for y in cuts_or_fills if y >= 0]

    y_cut = [y for y in cuts_or_fills if y < 0]

    return  sum(y_fill) - (4/5) * sum(y_cut)

#plotting

#x = existing_elevation[0]

#y = existing_elevation[1]

#plt.plot(x, y, linewidth=2.0)

#plt.show()

# case 1 code below: case 1 is for no linear section between the first and second station of the vertical curve

elevation = existing_elevation(horizontal_length, resolution, initial_elevation)

# design speed in ft / s

design_speed = 65 * (5280 / 3600)

# SSD of first vertical curve

design_elevation_difference = np.array([])

#  minimum design length of first vertical curve

for mid_slope in np.arange(-20, -1, 0.1):

    #for start_slope in np.arange(-20, -1, 1): determine if we can reduce cut and fill by 

    SSD_1 = SSD(design_speed, 0)

    #print(SSD_1)

    design_length_1 = design_length(0, mid_slope, SSD_1, "down")

    #print(design_length_1)

    SSD_2 = SSD(design_speed, mid_slope)

    design_length_2 = design_length(mid_slope, 0, SSD_2, "up")  

    if design_length_1 == "too large" or design_length_2 == "too large":

        print("at mid slope:", mid_slope, "value error, at least one design length exceeds 2000")

    elif design_length_1 + design_length_2 > 2000:

        print("at mid slope:", mid_slope, "value error, combined design lengths exceeds 2000")

    #else:

        #print("at mid slope:", mid_slope, "all is good, the design lengths are:", design_length_1," and ", design_length_2)


    first_curve = concave_down_vertical_curve(2100, 0, 0, mid_slope, 2000, 1000)

    second_curve = concave_up_vertical_curve(2000, 0, mid_slope, 0, 2000, 1000)

    total_curve_x = np.append(first_curve[0], second_curve[0])

    total_curve_y = np.append(first_curve[1], second_curve[1])

    # ensuring continuity / no jumps

    if abs(first_curve[1][-1] - second_curve[1][0]) < 0.1:

        cut_and_fill = cut_and_fill_case1(total_curve_y, elevation[1])

        design_elevation_difference = np.append(design_elevation_difference, cut_and_fill)

        if abs(cut_and_fill) < 3000:

            #saving data that fits minimum cut_and_fill

            print("the design midslope is:", mid_slope)

            print("the amount of cutting / filling required is:", cut_and_fill)

            saved_x = total_curve_x

            saved_y = total_curve_y

    #else:
        
        #print("jump between curve 1 and 2 detected! result invalid")

print(min(design_elevation_difference))

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(saved_x, saved_y, linewidth=2.0)

ax2.plot(elevation[0], elevation[1], linewidth=2.0)

plt.show()

        



        