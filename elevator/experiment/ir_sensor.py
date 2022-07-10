#!/usr/bin/env python3

from ev3dev2.console import Console
from ev3dev2.display import Display
from ev3dev2.sensor.lego import InfraredSensor
import ev3dev2.fonts as fonts

from time import sleep

console = Console()
#display = Display()

def output(text):
  console.text_at(text, reset_console=True, inverse=True)
  #console.draw.text((10,10), text, font=fonts.load('luBS14'))

#console = Console()
ir_sensor = InfraredSensor()

while True:
  distance_percent = ir_sensor.proximity
  print("Proximity " + str(distance_percent))
  #output(" IR Proximity: " + str(distance_percent))  
  
  sleep(3)
