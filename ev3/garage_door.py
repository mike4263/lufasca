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
from pybricks.messaging import BluetoothMailboxClient, LogicMailbox

# Initialize the EV3 Brick
ev3 = EV3Brick()

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'brick01'

client = BluetoothMailboxClient()
mbox = LogicMailbox('garage', client)
print('establishing connection...')
ev3.speaker.say("establishing connection")

client.connect(SERVER)
print('connected!')
ev3.speaker.say("connected")

piston_motor = Motor(Port.A)
lift_motor = Motor(Port.B)

while(1):
  mbox.wait()

  open_door = mbox.read()

  if open_door:
    piston_motor.run_angle(300, -91, then=Stop.HOLD, wait=True)
    wait(3000)
    lift_motor.run_time(1000, 17000)
    wait(23000)
    lift_motor.run_time(-1000, 17000)
    wait(3000)
    piston_motor.run_angle(300, 90, then=Stop.HOLD, wait=True)
    wait(3000)
  
  mbox.send(True)

