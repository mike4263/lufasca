#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import *
from pybricks.hubs import EV3Brick
from pybricks.parameters import *
from pybricks.tools import *
from mindsensorsPYB import DIST_ToF, mindsensors_i2c
from time import time
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
import math


# Initialize the EV3 Brick
ev3 = EV3Brick()

piston_motor = Motor(Port.A)
lift_motor = Motor(Port.B)

while(1):
  piston_motor.run_angle(300, -91, then=Stop.HOLD, wait=True)
  wait(3000)
  lift_motor.run_time(1000, 17000)
  wait(3000)
  lift_motor.run_time(-1000, 17000)
  wait(3000)
  piston_motor.run_angle(300, 90, then=Stop.HOLD, wait=True)
  wait(3000)

