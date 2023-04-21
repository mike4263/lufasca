#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import *
from pybricks.hubs import EV3Brick
from pybricks.parameters import *
from pybricks.tools import *
from mindsensorsPYB import DIST_ToF, mindsensors_i2c
from time import time


class TowerHeight():

    def __init__(self):
        pass

    def add(self, num):
        number = "{:.2f}".format(num)
        return number


# Initialize the EV3 Brick
ev3 = EV3Brick()
#streamerbot = Streamerbot()
ToF = DIST_ToF(Port.S1, 0x02)
tower = TowerHeight()

# Define the check_height_of_elevator() function


def check_height_of_elevator():
    laser_height = tower.add(ToF.readToFin())
    #print(laser_height)
    return laser_height


# Initialize the last_print_time timestamp variable
last_print_time = 0

while True:

    if Button.UP in ev3.buttons.pressed():
        ev3.screen.print("UP button pressed") # Call the check_height_of_elevator() function on each loop
        print("UP raised")

    if Button.DOWN in ev3.buttons.pressed():
        ev3.screen.print("DOWN button pressed")
        print("DOWN pressed")

    height = check_height_of_elevator()

    # Check if it's been 5 seconds since the last print time
    if time() - last_print_time >= 5:

        # Print the current height on the EV3DEV display
        ev3.screen.clear()
        ev3.screen.print("Height of elevator:")
        ev3.screen.print(height)

        print("Height: " + height)

        # Update the last_print_time timestamp variable
        last_print_time = time()

    # Add a 100ms delay between iterations to reduce CPU usage
    wait(1000)

