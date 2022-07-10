#!/usr/bin/env python3

from errno import EOVERFLOW
from pdb import post_mortem
from ev3dev2.console import Console
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import Motor, SpeedRPM
from time import sleep
import http.client, urllib.parse
#import urequests as requests


# IRA StreamerBot Action names
IRA_START_RECORDING = "ira-start-recording"
IRA_STOP_RECORDING = "ira-stop-recording"
IRA_TAKE_SCREENSHOT = "ira-take-screenshot"

motor = Motor()

def run_to_position(position):
  motor.on_to_position(SpeedRPM(5), position)




def invoke_streamerbot_action(action_name, raw_input="None"):
  conn = http.client.HTTPConnection("192.168.1.23:6286")
  #conn = http.client.HTTPConnection("perch.host.box1.org:8000")

  body_text = """
  {
  "action": {
    "name": "%s"
  },
  "args": {
    "input": "%s",
  }
}
  """ % (action_name, raw_input)
  conn.request("POST", "/DoAction", body_text)

run_to_position(0)

run_to_position(35)
#invoke_streamerbot_action(IRA_START_RECORDING)

run_to_position(325)
#invoke_streamerbot_action(IRA_STOP_RECORDING)

sleep(5)
run_to_position(180)
#invoke_streamerbot_action(IRA_TAKE_SCREENSHOT)

run_to_position(0)