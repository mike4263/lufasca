#!/usr/bin/env python3

from errno import EOVERFLOW
from pdb import post_mortem
from ev3dev2.console import Console
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import Motor, SpeedRPM, OUTPUT_C

from time import sleep
import http.client, urllib.parse
#import urequests as requests


# IRA StreamerBot Action names
IRA_START_RECORDING_ID = "e7bac8b9-ad08-4301-89b2-0146dc664afb"
IRA_START_RECORDING_NAME = "ira-start-recording"
IRA_STOP_RECORDING_ID = "7366c8c9-4713-4328-adf7-688884be8c37"
IRA_STOP_RECORDING_NAME = "ira-stop-recording"
IRA_TAKE_SCREENSHOT_ID = "271153fa-f448-4f2f-acad-0dbfcad4de74"
IRA_TAKE_SCREENSHOT_NAME = "ira-take-screenshot"

motor = Motor(OUTPUT_C)

def run_to_position(position):
  print("Moving to " + str(position))
  motor.on_to_position(SpeedRPM(5), position)

def invoke_streamerbot_action(action_id, action_name, raw_input="None"):
  conn = http.client.HTTPConnection("192.168.1.23:6291")
  #conn = http.client.HTTPConnection("perch.host.box1.org:8000")

  body_text = """
  {
  "action": {
    "id": "%s",
    "name": "%s"
  },
  "args": {
    "key": "%s",
  }
}
  """ % (action_id, action_name, raw_input)
  conn.request("POST", "/DoAction", body_text)

run_to_position(0)

invoke_streamerbot_action(IRA_START_RECORDING_ID, IRA_START_RECORDING_NAME)

run_to_position(360)
invoke_streamerbot_action(IRA_STOP_RECORDING_ID, IRA_STOP_RECORDING_NAME)

sleep(5)
invoke_streamerbot_action(IRA_TAKE_SCREENSHOT_ID, IRA_TAKE_SCREENSHOT_NAME)
