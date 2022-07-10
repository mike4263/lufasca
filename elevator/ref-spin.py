#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.console import Console
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import Motor, SpeedRPM
from time import sleep

import pdb

console = Console()

console.reset_console()
console.text_at("Cherry Blossom", column=1, row=5,
  reset_console=True)

touch = TouchSensor()
motor = Motor()

def run_to_position(position):
  motor.on_to_position(SpeedRPM(5), position)

run_to_position(0)
sleep(5)
run_to_position(35)
sleep(5)

run_to_position(180)
sleep(5)

run_to_position(325)
sleep(5)
run_to_position(0)


print(motor.commands)

# (Pdb) ['run-forever', 'run-to-abs-pos', 'run-to-rel-pos', 'run-timed', 'run-direct', 'stop', 'reset']
exit(0)
while True:
  if touch.is_pressed:
    break
  motor.on_for_seconds(SpeedRPM(20), 1)

sound = Sound()
sound.speak("hello twitch chat ")

console.text_at("Redwood", column=1, row=6)
sleep(5)