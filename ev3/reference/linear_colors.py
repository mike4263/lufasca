import math

# Distance range in inches
min_distance = 3
max_distance = 35

# Color values in hexadecimal format
blue_color = 0x0000FF
green_color = 0x00FF00
red_color = 0xFF0000

def map_range(value, from_min, from_max, to_min, to_max):
    # Linearly interpolate the value from one range to another
    return math.floor((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)


for distance in range(min_distance, max_distance+1):

    color = map_range(distance, min_distance, max_distance, blue_color, red_color)
    #hex_str = "{:06X}".format(color)
    hex_str = "%06X" % color
    print(hex_str)

    red = hex_str[0:2]
    green = hex_str[2:4]
    blue = hex_str[4:6]
    print(red)
    print(green)
    print(blue)
    print(blue.encode())