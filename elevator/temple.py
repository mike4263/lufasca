#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, InfraredSensor )
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


mids_catch = Motor(Port.A)
above_catch = Motor(Port.B)
above_catch_sensor = TouchSensor(Port.S1)

#above_catch.run_time(100, 2300, wait=False)
# Write your program here.
ev3.speaker.beep()

#mids_catch.run_time(200, 1200)

while ( above_catch_sensor.pressed() == False):
    sleep(.21)

ev3.speaker.beep()

#mids_catch.run_time(200, 1200)